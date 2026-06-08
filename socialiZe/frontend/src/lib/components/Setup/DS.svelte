<script lang="ts">
    import { writable, type Writable } from "svelte/store";
    import { onMount } from "svelte";
    import { worker } from "$lib/helpers/js/sharedWorker";

    const dotProperties: Writable<{
        radius: number;
        colour: string;
        opacity: number;
    }> = writable({
        radius: 10,
        colour: "#000000",
        opacity: 1,
    });

    function updateRadius(): number {
        return $dotProperties.radius;
    }

    function updateColour(): string {
        return $dotProperties.colour;
    }

    function updateOpacity(): number {
        return $dotProperties.opacity;
    }

    function updateProperties(): void {
        worker.port.postMessage({
            type: "SET_DOT_PROPERTIES",
            data: {
                size: updateRadius(),
                colour: updateColour(),
                opacity: updateOpacity(), 
            }, 
        });
    }

    onMount(() => {
        if (typeof window !== 'undefined') {
            worker.port.start();
            worker.port.postMessage({ type: "READY" });

            updateProperties();
        }
    });
</script>

<div class="flex w-full rounded-xl items-center {$$props.class}">
    <!-- Settings -->
    <div class="flex flex-col justify-center w-full pr-2">
        <div>
            <label for="radius" class="font-semibold">Radius:</label>
            <input id="radius" type="number" min="0" max="100" on:change={updateProperties} bind:value={$dotProperties.radius} class="input" />
        </div>

        <div class="py-2">
            <label for="opacity" class="font-semibold">Opacity:</label>
            <input id="opacity" type="range" min="0" max="1" step="0.01" on:change={updateProperties} bind:value={$dotProperties.opacity} />
        </div>

        <div>
            <label for="colour" class="font-semibold">Colour:</label>
            <div class="grid grid-cols-[auto_1fr] gap-2">
                <input id="colour" class="input" type="color" on:change={updateProperties} bind:value={$dotProperties.colour} />
                <input class="input" type="text" bind:value={$dotProperties.colour} readonly tabindex="-1" />
            </div>
        </div>
    </div>
</div>