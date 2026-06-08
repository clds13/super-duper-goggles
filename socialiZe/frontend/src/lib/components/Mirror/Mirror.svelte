<script lang="ts">
    import { onMount } from "svelte";
    import { type Writable, writable } from "svelte/store";
    import { stimulus } from "$lib/stores/stimulus";

    let dotElement: SVGCircleElement;
    let divWidth: number;

    let radius: Writable<number> = writable(0);
    let opacity: Writable<number> = writable(0);
    let colour: Writable<string> = writable("black");

    export let key: string = "manualDotSyncData";
    export let visible: boolean = false;
    export let twoDots: boolean = true;
    export let showTrail: boolean = false;

    export const percentage: Writable<number> = writable(0);
    export let positionData: {
        x: number;
        y: number;
        angle: number;
        timestamp: number;
    }[] = [];
    export let logPositionData: boolean = false;

    const FPS: number = 30;
    const FRAME_TIME: number = 1000 / FPS;
    let frameNumber: number = 0;
    let frameTimeElapsed: number = 0;

    let lastUpdateTime = Date.now();
    let lastData: any = {};

    // NEW *****
    const dotX: Writable<number> = writable(0);
    const dotY: Writable<number> = writable(0);
    export let remainingTime: number = 0;
    export let totalTime: number = 0;

    // Second dot
    const dotX2: Writable<number> = writable(0);
    const dotY2: Writable<number> = writable(0);
    let dotElement2: SVGCircleElement;

    // Get the time per frame in MS (approx 33.33ms)
    const TIME_PER_FRAME: number = 1000 / FPS;
    const TOTAL_TIME_MS: number = totalTime * 1000;

    let transitionStarted = false;

    let startTime: number | null = null;
    let lastLoggedFrame: number | null = null;


    // Modify stimulus based on the dot properties
    $: {
        
        if (dotElement) {
            $stimulus = {
                colour: $colour,
                opacity: $opacity,
                radius: $radius,
            };
            // console.log(`The dot is '${$stimulus.colour}' with opacity ${$stimulus.opacity} and radius ${$stimulus.radius}`);
        }
        
    }


    function logPosition() {
        if (!transitionStarted) {
            return;
        }

        let rect = dotElement.getBoundingClientRect();

        // If the timer hasn't started yet, start it now
        if (startTime === null) {
            startTime = performance.now();
        }

        // Calculate the elapsed time in milliseconds
        const timeElapsed = performance.now() - startTime;

        // Calculate the current frame number
        const frameNumber = Math.floor(timeElapsed / TIME_PER_FRAME);

        // Only log the position if this is a new frame
        if (frameNumber !== lastLoggedFrame) {
            console.log("🚀 ~ logPosition ~ frameNumber:", frameNumber);

            // Add the dot's position to the positionData array with the frame number
            if (logPositionData) {
                positionData = [
                    ...positionData,
                    {
                        x: rect.left / divWidth,
                        y: rect.top / divWidth,
                        angle: 0,
                        timestamp: frameNumber,
                    },
                ];
            }

            // Update the last logged frame number
            lastLoggedFrame = frameNumber;
        }

        requestAnimationFrame(logPosition);
    }

    function calculatePercentage() {
        const outerRadius: number = divWidth / 2 - divWidth / 50;
        const innerRadius: number = $radius;

        const percentageValue: number =
            Math.pow(innerRadius / outerRadius, 2) * 100;

        $percentage = percentageValue;
    }

    const handleLocalStorageChange = () => {
        const stimulusSyncData = localStorage.getItem(key);

        if (!stimulusSyncData) {
            return;
        }

        if (!visible) {
            return;
        }

        // Calculate the percent size of the dot
        calculatePercentage();

        if (key === "manualDotSyncData") {
            const data = JSON.parse(stimulusSyncData);
            const angle: number = data.angle;
            const pathRadius: number = data.pathRadius;
            const centerX: number = divWidth / 2;
            const centerY: number = divWidth / 2;

            // Update the dot position
            $dotX = centerX + pathRadius * centerX * Math.cos(angle);
            $dotY = centerY + pathRadius * centerY * Math.sin(angle);

            // Set the dot's position
            dotElement.setAttribute("cx", $dotX.toString());
            dotElement.setAttribute("cy", $dotY.toString());

            $radius = data.radius * divWidth;
            $opacity = data.opacity;
            // $colour = data.colour;
        } else if (key === "fileDotSyncData") {
            const data = JSON.parse(stimulusSyncData);

            // Update the dot position
            $dotX = (data.x * divWidth);
            $dotY = (data.y * divWidth);

            // Set the dot's position
            dotElement.setAttribute("cx", $dotX.toString());
            dotElement.setAttribute("cy", $dotY.toString());

            // Check if two dots should be visible
            if (twoDots) {
                // Set dotX2 and dotY2 to dotX and dotY transformed by flipping on the x-axis and y-axis
                $dotX2 = divWidth - $dotX;
                $dotY2 = divWidth - $dotY;

                // Set the second dot's position
                dotElement2.setAttribute("cx", $dotX2.toString());
                dotElement2.setAttribute("cy", $dotY2.toString());
            }

            // Update the dot parameters
            $radius = data.radius * divWidth;
            $opacity = data.opacity;
            $colour = data.colour;

            if (logPositionData) {
                positionData = [
                    ...positionData,
                    {
                        x: $dotX,
                        y: $dotY,
                        angle: 0,
                        timestamp: frameNumber,
                    },
                ];
            }

            frameNumber++;

            // Update the last logged frame number
            lastLoggedFrame = frameNumber;
        } else if (key === "videoSyncData") {
            const data = JSON.parse(stimulusSyncData);
        }
    };

    onMount(() => {
        // Try to get the dot element
        const checkDotInterval = setInterval(() => {
            if (dotElement) {
                console.log("Dot element exists");


                if (key === "manualDotSyncData") {
                    dotElement.addEventListener("transitionstart", () => {
                        transitionStarted = true;
                        logPosition();
                    });

                    dotElement.addEventListener("transitionend", () => {
                        transitionStarted = false;
                    });
                } else if (key === "fileDotSyncData") {
                    // ***
                }

                clearInterval(checkDotInterval);
            }

            if (dotElement2) {
                console.log("Second dot element exists");
            }
        }, 1000);

        window.addEventListener("storage", handleLocalStorageChange);
    });
</script>

<div class="flex w-full h-full {$$props.class}">
    <div
        class="flex w-full h-full items-center justify-center"
        bind:clientWidth={divWidth}
    >
        <svg width={divWidth} height={divWidth}>
            <circle
                cx={divWidth / 2}
                cy={divWidth / 2}
                r={divWidth / 2 - divWidth / 50}
                fill="white"
            />
            {#if visible}
                {#if twoDots}
                    <!-- Dot One -->
                    <circle
                        bind:this={dotElement}
                        r={$radius}
                        fill={$colour}
                        style={"opacity: " + $opacity}
                        class={key === "manualDotSyncData"
                            ? "transition-all duration-500"
                            : ""}
                    />
                    <!-- Dot Two -->
                    <circle
                        bind:this={dotElement2}
                        r={$radius}
                        fill={$colour}
                        style={"opacity: " + $opacity}
                        class={key === "manualDotSyncData"
                            ? "transition-all duration-500"
                            : ""}
                    />
                {:else}
                    <!-- Single Dot -->
                    <circle
                        bind:this={dotElement}
                        r={$radius}
                        fill={$colour}
                        style={"opacity: " + $opacity}
                        class={key === "manualDotSyncData"
                            ? "transition-all duration-500"
                            : ""}
                    />
                {/if}
            {/if}
        </svg>
    </div>
</div>
