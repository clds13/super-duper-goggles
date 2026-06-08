<script lang="ts">
    import { onMount } from "svelte";
    import { writable, type Writable } from "svelte/store";
    import { worker } from "$lib/helpers/js/sharedWorker";
    import { initializeSvg, initializeSvg2, initializeDot } from "$lib/helpers/configureSvg";
    import { animateSvg, scaleData } from "$lib/helpers/animationHelper";

    const videoDimensions = { width: 1920, height: 1200 };

    let svgWidth: number;
    let svgHeight: number;
    let svgElement: SVGSVGElement;
    let dotElement: SVGCircleElement;

    // Recording properties
    let adaptationDuration: number = 0;
    let fadeInDuration: number = 0;
    let duration: number = 0;
    let cd: Writable<number> = writable(0);
    let totalCountdown: number = 0;

    let jumpFactor: number;
    let speed: number;
    let coordinates: { x: number; y: number, frame: number }[] = [];
    let firstCoordinate: { x: number, y: number, frame: number };
    let firstCoordinateScaled: { x: number, y: number, frame: number } = { x: 0, y: 0, frame: 0 };

    let timeout: NodeJS.Timeout;
    
    export let pathType: string;

    // Dot properties
    let dotSize: number = 5;
    let dotColour: string = "black";
    let dotOpacity: number = 1;

    onMount(() => {
        if (typeof window !== 'undefined') {
            worker.port.start();
            worker.port.postMessage({ type: "READY_POPOUT" });

            window.addEventListener('keydown', (event) => {
                if (event.code === 'Space') {
                    worker.port.postMessage({ type: "START_TRIAL" });
                }
            });

            worker.port.addEventListener('message', (event: MessageEvent) => {
                console.log('Message received:', event.data.type);
                if (event.data.type === 'START_TRIAL') {
                    countdown();
                } else if (event.data.type === 'POPOUT_PROPERTIES') {
                    const data = event.data.data;

                    // Get the different properties
                    const stimulusProperties = data.stimulusProperties;
                    const recordingProperties = data.recordingProperties;

                    // Set the dot properties
                    const dotProperties = stimulusProperties.dotProperties;
                    dotSize = dotProperties.size;
                    dotColour = dotProperties.colour;
                    dotOpacity = dotProperties.opacity;

                    // Set the path type
                    jumpFactor = stimulusProperties.jumpFactor;
                    speed = stimulusProperties.speed;
                    coordinates = stimulusProperties.coordinates;

                    // Set the recording properties
                    adaptationDuration = recordingProperties.adaptationDuration;
                    fadeInDuration = recordingProperties.fadeInDuration;
                    duration = recordingProperties.duration;
                    totalCountdown = fadeInDuration + duration + adaptationDuration;
                } else if (event.data.type === 'FIRST_COORDINATE') {
                    firstCoordinate = event.data.data.coordinate;

                    const radius = Math.min(svgWidth, svgHeight) / 2;
                    const centerX = svgWidth / 2;
                    const centerY = svgHeight / 2;

                    if (pathType === "file") {
                        const x = (firstCoordinate.x / videoDimensions.width) * svgWidth;
                        const y = (firstCoordinate.y / videoDimensions.height) * svgHeight;
                        firstCoordinateScaled.x = x;
                        firstCoordinateScaled.y = y;
                    } else {
                        // Assuming the original Lissajous path was generated with a range of -100 to 100

                        // Scale the data point to 50% of the radius of the circle, maintaining the aspect ratio
                        const scale = (radius / 2) / 100; // 100 is half of the originalRange
                        const x = centerX + firstCoordinate.x * scale;
                        const y = centerY + firstCoordinate.y * scale;
                        firstCoordinateScaled.x = x;
                        firstCoordinateScaled.y = y;
                    }
                    
                    dotElement.setAttribute("cx", firstCoordinateScaled.x.toString());
                    dotElement.setAttribute("cy", firstCoordinateScaled.y.toString());
                    dotElement.style.fill = dotColour;
                }
            });
        }

         // Initialize SVG elements
         if (!dotElement) {
            svgWidth = svgElement.clientWidth;
            svgHeight = svgElement.clientHeight;
            dotElement = initializeDot(svgElement) as SVGCircleElement;
            setTimeout(() => {
                dotElement = initializeSvg2(dotElement, Math.min(adaptationDuration, 5));
            }, 1000);
        }
    });

    /**
     * Starts a countdown timer for duration seconds. When the countdown
     * finishes, the path of the dot is reset through the worker.
     * 
     * @returns void
     */
    function countdown(): void {
        fadeIn(fadeInDuration);
        const interval = setInterval(() => {
            totalCountdown -= 1;
            if (totalCountdown <= 0) {
                clearInterval(interval);
                clearTimeout(timeout);

                // Fire the event to reset the animation
                worker.port.postMessage({ type: "STOP_ANIMATION" });
                dotElement.setAttribute("opacity", "0");
            }

            // Begin fading in the dot
            if (totalCountdown === (duration + Math.min(adaptationDuration, 5))) {
                // Set the dot properties
                dotElement.setAttribute("r", dotSize.toString());
                dotElement.setAttribute("fill", dotColour);
                dotElement.setAttribute("opacity", dotOpacity.toString());
                dotElement.setAttribute("cx", firstCoordinateScaled.x.toString());
                dotElement.setAttribute("cy", firstCoordinateScaled.y.toString());
            }

            // Start the animation
            if (totalCountdown === duration) {

                // Fire the event to start the animation
                worker.port.postMessage({ type: "RESTART_ANIMATION" });

                // Animate the SVG element
                if (coordinates.length > 0) {
                    const newCoordinates = coordinates.filter((_: any, index: number) => index % jumpFactor === 0);
                    animate(newCoordinates, 0, jumpFactor);
                }
            }
        }, 1000);
    }

    /**
     * Fades in the SVG element over a duration of seconds.
     * 
     * @param seconds - The duration of the fade in animation in seconds
     * @returns void
    */
    function fadeIn(seconds: number): void {
        svgElement.style.transition = `background-color ${seconds}s`;

        // Add bg-white
        svgElement.classList.add("bg-white");
    }

    /**
     * Animates the SVG elements in the DotPreview component.
     * 
     * @param {Array<{ x: number; y: number, frame: number }>} pathCoordinates - The array of path coordinates to animate.
     * @param {number} currentIndex - The current index in the pathCoordinates array.
     * @param {number} jumpFactor - The number of frames to skip during animation.
     */
     function animate(
        pathCoordinates: { x: number; y: number, frame: number }[],
        currentIndex: number,
        jumpFactor: number
    ) {
        // if (currentIndex === 0 ){
        //     console.time('animate');
        // }

        // Animate the SVG element
        animateSvg(pathCoordinates[Math.floor(currentIndex)], pathType, videoDimensions, svgWidth, svgHeight, dotElement);
        let nextIndex = (currentIndex + 1 / jumpFactor) % pathCoordinates.length;

        // if (nextIndex < currentIndex) {
        //     console.timeEnd('animate');
        //     console.time('animate');
        // }

        // Clear the timeout if it exists
        if (timeout) {
            clearTimeout(timeout);
        }

        // Call animate again after a delay
        timeout = setTimeout(() => animate(pathCoordinates, nextIndex, jumpFactor), 1000 / 60);
    }
</script>

<div class="flex w-full items-center justify-center {$$props.class}">
    <!-- Text Element at top Right Corner with countdown -->
    <div class="absolute top-0 right-0 p-2">
        <p class="{totalCountdown - duration <= 0 ? 'text-red-500' : 'text-white'} font-bold">{totalCountdown}</p>
    </div>

    <div class="flex w-full items-center justify-center {$$props.class}">
        <svg bind:this={svgElement} class="w-full h-full rounded-full border-2 border-white">
        </svg>
    </div>
</div>