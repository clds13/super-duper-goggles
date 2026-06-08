<script lang="ts">
    import { onMount } from "svelte";
    import { worker } from "$lib/helpers/js/sharedWorker";


    let path: string;
    let pathJumpFactor: number = 10;
    let pathSpeed: number = 30;

    let jumpFactorMin: number = 1;
    let jumpFactorMax: number = 500;

    let speedMin: number = 0.5;
    let speedMax: number = 60;

    let pathType: "predefined" | "file" = "predefined";

    function updatePath(): void {


        if (pathType === "predefined") {
            worker.port.postMessage({
                type: "SET_DOT_PATH",
                data: {
                    pathType: "predefined",
                    pathData: {
                        type: path,
                        speed: pathSpeed,
                        jumpFactor: pathJumpFactor
                    }
                },
            });
            return;
        } else {
            worker.port.postMessage({
                type: "SET_DOT_PATH",
                data: {
                    pathType: "file",
                    pathData: {
                        type: "file",
                        speed: pathSpeed,
                        jumpFactor: pathJumpFactor
                    },
                    resend: true
                },
            });
        }
    }

    onMount(() => {
        if (typeof window !== 'undefined') {
            worker.port.start();
            worker.port.postMessage({ type: "READY" });

            worker.port.addEventListener('message', (event: MessageEvent) => {
                if (event.data.type == "DOT_PATH") {
                    const data = event.data.data;
                    pathType = data.pathType;
                }
            });

            updatePath();
        }
    });
</script>

<div class="flex w-full rounded-xl items-center {$$props.class}">
    <!-- Settings -->
    <div class="flex flex-col w-full">
        <!-- Dropdown -->
        <div class="">
            <label for="pathType" class="font-semibold">Path Type:</label>
            <select id="pathType" class="select" bind:value={path} on:change={updatePath}>
                <option value="circular">Circular</option>
                <option value="fish">Fish-like</option>
                <option value="lissajous">Lissajous</option>
            </select>
        </div>
        <!-- Slider for Path Speed -->
        <div class="py-2">
            <label for="pathSpeed" class="font-semibold">Speed:</label>
            <div class="flex justify-between w-full items-center">
                <span class="pr-1">{speedMin}</span>
                <input class="input text-center" title="pathSpeed" type="number" bind:value={pathSpeed} on:change={updatePath} step="1.0" min={speedMin} max={speedMax}>
                <span class="pl-1">{speedMax}</span>
            </div>
        </div>
        <!-- Slider for Jump Factor -->
        <div class="">
            <label for="pathJumpFactor" class="font-semibold">Jump Factor:</label>
            <div class="flex justify-between w-full items-center">
                <span class="pr-1">{jumpFactorMin}</span>
                <input class="input text-center" title="pathJumpFactor" type="number" bind:value={pathJumpFactor} on:change={updatePath} step="0.5" min={jumpFactorMin} max={jumpFactorMax}>
                <span class="pl-1">{jumpFactorMax}</span>
            </div>
        </div>
    </div>
</div>