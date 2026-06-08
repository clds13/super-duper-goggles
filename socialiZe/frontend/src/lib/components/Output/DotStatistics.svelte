<script lang="ts">
    import { onMount } from "svelte";
    import { writable, type Writable } from "svelte/store";
    import { worker } from "$lib/helpers/js/sharedWorker";
    import StatCard from "../Dashboard/StatCard.svelte";
    import { parseDotPathMessage } from "$lib/helpers/workerParsers";
    import { addAPIProvider } from "@iconify/svelte";


    const dotSize: Writable<number> = writable(0);
    const remainingTime: Writable<number> = writable(0);
    const timeCaption: string[] = [
        "Fade In",
        "Adaptation",
        "Active",
        "Inactive"
    ]
    let remainingTimeCaption: string = "Inactive";

    let pathTypeCaption: string;
    let pathSpeedCaption: string;
    let pathJumpFactorCaption: string;
    let dotProperties: { radius: number; colour: string; opacity: number } = {
        radius: 5,
        colour: "black",
        opacity: 1,
    };

    onMount(() => {

        if (typeof window !== 'undefined') {
            worker.port.start();
            worker.port.postMessage({ type: "READY" });

            worker.port.addEventListener('message', (event: MessageEvent) => {
                if (event.data.type === "DOT_PATH") {
                    const { pathType, pathSpeed, pathJumpFactor } = parseDotPathMessage(event);

                    pathTypeCaption = pathType.charAt(0).toUpperCase() + pathType.slice(1);
                    pathSpeedCaption = pathSpeed.toString();
                    pathJumpFactorCaption = pathJumpFactor.toString();
                } else if (event.data.type === "SET_DOT_PROPERTIES") {
                    const data = event.data.data;
                    const size = data.size;
                    const colour = data.colour;
                    const opacity = data.opacity;

                    dotProperties.radius = size;
                    dotProperties.colour = colour;
                    dotProperties.opacity = opacity;
                } else if (event.data.type === 'START_TRIAL') {
                    const data = event.data.data;
                    const duration = data.duration;
                    const adaptationDuration = data.adaptationDuration;
                    const fadeInDuration = data.fadeInDuration;
                    // const delay = data.delay;

                    remainingTimeCaption = timeCaption[0];

                    remainingTime.set(fadeInDuration);
                    let countdown = setInterval(() => {
                        if ($remainingTime > 0) {
                            $remainingTime -= 1;
                        } else {
                            clearInterval(countdown);

                            $remainingTime = adaptationDuration - 1;
                            remainingTimeCaption = timeCaption[1];
                            countdown = setInterval(() => {
                                if ($remainingTime > 0) {
                                    $remainingTime -= 1;
                                } else {
                                    clearInterval(countdown);

                                    $remainingTime = duration - 1;
                                    remainingTimeCaption = timeCaption[2];
                                    countdown = setInterval(() => {
                                        if ($remainingTime > 0) {
                                            $remainingTime -= 1;
                                        } else {
                                            clearInterval(countdown);
                                            remainingTimeCaption = timeCaption[3];
                                        }
                                    }, 1000);
                                }
                            }, 1000);
                        }
                    }, 1000);
                }
            });
        }

        window.addEventListener('message', (event) => {
            if (event.data.type === "SYNC_DUR") {
                console.log(event.data);

                const duration: number = event.data.duration;
                const delay: number = event.data.delay;

                // Set the caption
                remainingTimeCaption = timeCaption[0];

                // Start the delay countdown
                $remainingTime = delay;
                let countdown = setInterval(() => {
                    if ($remainingTime > 0) {
                        $remainingTime -= 1;
                    } else {
                        clearInterval(countdown);

                        // Once the delay is over, start the duration countdown
                        $remainingTime = duration;
                        remainingTimeCaption = timeCaption[1];
                        countdown = setInterval(() => {
                            if ($remainingTime > 0) {
                                $remainingTime -= 1;
                            } else {
                                clearInterval(countdown);
                                remainingTimeCaption = timeCaption[2];
                            }
                        }, 1000);
                    }
                }, 1000);
            } else if (event.data.type === "DOT_SIZE") {
                $dotSize = event.data.size
            }
        })
    })
</script>


<div class="flex flex-row w-full h-full">
    <div class="flex flex-col w-full">
        <h1 class="text-2xl font-semibold mb-2">
            Dot
        </h1>

        <div class="flex flex-row w-full items-center justify-between">
            <StatCard icon="mdi:paint-outline" iconSize="w-2/3 h-2/3" title="Colour" value={dotProperties.colour} class="w-1/4 h-full" />
            <StatCard icon="mdi:arrow-split-vertical" iconSize="w-2/3 h-2/3" title="Diameter" value={dotProperties.radius.toString()} class="w-1/4 h-full" />
            <StatCard icon="mdi:alpha-o-circle-outline" iconSize="w-2/3 h-2/3" title="Opacity" value={dotProperties.opacity.toString()} class="w-1/4 h-full" />
        </div>
    </div>

    <span class="divider-vertical mx-4" />

    <div class="flex flex-col w-full">
        <h1 class="text-2xl font-semibold mb-2">
            Path
        </h1>

        <div class="flex flex-row w-full items-center justify-between">
            <StatCard icon="mdi:shape" iconSize="w-2/3 h-2/3" title="Type" value={pathTypeCaption} class="w-1/4 h-full" />
            <StatCard icon="mdi:speedometer" iconSize="w-2/3 h-2/3" title="Speed" value={pathSpeedCaption} class="w-1/4 h-full" />
            <StatCard icon="mdi:waveform" iconSize="w-2/3 h-2/3" title="Jump" value={pathJumpFactorCaption} class="w-1/4 h-full" />
        </div>
    </div>

    <span class="divider-vertical mx-4" />

    <div class="flex flex-col w-full">
        <h1 class="text-2xl font-semibold mb-2">
            Recording
        </h1>

        <div class="flex flex-row w-full items-center justify-between">
            <StatCard icon="mdi:clock" iconSize="w-2/3 h-2/3" title={remainingTimeCaption} value={$remainingTime.toString()} class="w-1/4 h-full" />
        </div>
    </div>
</div>