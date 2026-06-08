<script lang="ts">
    import { onMount } from "svelte";
    import { worker } from "$lib/helpers/js/sharedWorker";
    import { initializeSvg, setDotProperties } from "$lib/helpers/configureSvg";
    import { animateSvg, scaleData } from "$lib/helpers/animationHelper";
    import { calculateTotalDistance } from "$lib/helpers/speedHelper";

    const videoDimensions = { width: 1920, height: 1200 };

    let svgWidth: number;
    let svgHeight: number;

    let svgElement: SVGSVGElement;
    let dotElement: SVGCircleElement;
    let timeout: NodeJS.Timeout;

    export let pathType: string;

    // Path parameters
    let newCoordinates: { x: number; y: number, frame: number }[] = [];
    let pathJumpFactor: number;

    // 1px = 0.12mm
    const CONVERSION_FACTOR: number = 1;
    const SPEED_MULTIPLIER: number = 1;
    const CSV_ACQUISITION_FPS: number = 20;

    let totalDistance: number;

    // Timers
    let startTime: number;


    onMount(() => {
        if (typeof window !== "undefined") {
            worker.port.start();
            worker.port.postMessage({ type: "READY" });

            worker.port.addEventListener('message', (event: MessageEvent) => {
                if (event.data.type == "DOT_PATH") {
                    const data = event.data.data;
                    const pathData = data.pathData;
                    const pathCoordinates = data.pathCoordinates;
                    const pathSpeed = pathData.speed;
                    pathJumpFactor = pathData.jumpFactor;

                    if (pathCoordinates.length > 0) {
                        newCoordinates = pathCoordinates.filter((_: any, index: number) => index % pathJumpFactor === 0);
                        // Calculate the total distance of the path
                        totalDistance = calculateTotalDistance(newCoordinates, CONVERSION_FACTOR);
                        animate(newCoordinates, 0, pathJumpFactor, true);
                    }
                } else if (event.data.type === "SET_DOT_PROPERTIES") {
                    const data = event.data.data;
                    dotElement.setAttribute("r", data.size.toString());
                    dotElement.setAttribute("fill", data.colour);
                    dotElement.setAttribute("opacity", data.opacity.toString());
                } else if (event.data.type === "RESET") {
                    if (timeout) {
                        clearTimeout(timeout);
                    }
                } else if (event.data.type === "RESTART_ANIMATION") {
                    if (timeout) {
                        clearTimeout(timeout);
                    }
                    animate(newCoordinates, 0, pathJumpFactor);
                } else if (event.data.type === "STOP_ANIMATION") {
                    if (timeout) {
                        clearTimeout(timeout);
                    }
                }
            });
        }

        // Initialize SVG elements
        if (!dotElement) {
            svgWidth = svgElement.clientWidth;
            svgHeight = svgElement.clientHeight;
            dotElement = initializeSvg(svgElement) as SVGCircleElement;
        }
    });

    /**
     * Animates the SVG elements in the DotPreview component.
     * 
     * @param {Array<{ x: number; y: number, frame: number }>} pathCoordinates - The array of path coordinates to animate.
     * @param {number} currentIndex - The current index in the pathCoordinates array.
     * @param {number} jumpFactor - The number of frames to skip during animation.
     * @param {boolean} timeAnimation - Optional parameter to specify whether to time the animation or not.
     */
    function animate(
        pathCoordinates: { x: number; y: number, frame: number }[],
        currentIndex: number,
        jumpFactor: number,
        timeAnimation: boolean = false
    ) {
        if (timeAnimation && currentIndex === 0) {
            console.time('animate');

            // Start a timer with performance.now()
            startTime = performance.now();
        }

        // Animate the SVG element
        animateSvg(pathCoordinates[Math.floor(currentIndex)], pathType, videoDimensions, svgWidth, svgHeight, dotElement);
        let nextIndex = (currentIndex + 1 / jumpFactor) % pathCoordinates.length;

        if (timeAnimation && nextIndex < currentIndex) {
            console.timeEnd('animate');

            // Calculate the time taken to animate the path
            const endTime = performance.now();
            const timeTaken = endTime - startTime;

            // Convert the speed to scientific notation
            const speed = (totalDistance / timeTaken).toExponential(2);

            console.log(`Time taken: ${timeTaken.toFixed(2)} ms\nTotal distance: ${totalDistance.toFixed(2)} mm\nAverage speed: ${speed} mm/s`);

            console.time('animate');
            startTime = performance.now();
        }

        // Clear the timeout if it exists
        if (timeout) {
            clearTimeout(timeout);
        }

        // Call animate again after a delay
        timeout = setTimeout(() => animate(pathCoordinates, nextIndex, jumpFactor, timeAnimation), (1000 / CSV_ACQUISITION_FPS) * SPEED_MULTIPLIER);
    }
</script>


<div class="flex w-full items-center justify-center {$$props.class}">
    <svg bind:this={svgElement} class="w-full h-full bg-white rounded-full">
    </svg>
</div>

