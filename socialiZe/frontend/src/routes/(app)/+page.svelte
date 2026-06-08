<script lang="ts">
    import CameraView from "$lib/components/CameraView/CameraView.svelte";
    import Icon from "@iconify/svelte";
    import DotStatistics from "$lib/components/Output/DotStatistics.svelte";
    import { RadioGroup, RadioItem } from "@skeletonlabs/skeleton";
    import DP from "$lib/components/DotPreview/DP.svelte";
    import FilePanel from "$lib/components/Panels/FilePanel.svelte";
    import DotPanel from "$lib/components/Panels/DotPanel.svelte";


    let stimulusType: "dot" | "video" | "file" = "dot";
</script>

<div class="grid grid-cols-3">
    <div
        class="flex flex-col overflow-y-scroll col-span-1 items-center h-[75vh] mx-2"
    >
        <h1 class="text-4xl font-semibold px-4 py-2">Setup</h1>

        <div class="flex flex-row items-center w-full mb-2 px-4">
            {#if stimulusType === "dot"}
                <Icon icon="mdi:circle" class="w-6 h-6" />
            {:else if stimulusType === "video"}
                <Icon icon="mdi:video" class="w-6 h-6" />
            {:else if stimulusType === "file"}
                <Icon icon="mdi:file" class="w-6 h-6" />
            {/if}
            <h2 class="text-2xl font-semibold ml-2">Stimulus Type</h2>
        </div>

        <RadioGroup class="flex w-full mb-2">
            <RadioItem
                bind:group={stimulusType}
                value="dot"
                class="w-full"
                name="stimulusType"
            >
                Dot
            </RadioItem>
            <RadioItem
                bind:group={stimulusType}
                value="video"
                class="w-full"
                name="stimulusType"
            >
                Video
            </RadioItem>
            <RadioItem
                bind:group={stimulusType}
                value="file"
                class="w-full"
                name="stimulusType"
            >
                File
            </RadioItem>
        </RadioGroup>
        {#if stimulusType === "dot"}
        <DotPanel />
        {:else if stimulusType === "video"}
        <p>
            Coming soon...
        </p>
        {:else if stimulusType === "file"}
            <FilePanel />
        {/if}
    </div>

    <div class="flex flex-col col-span-2">
        <div class="flex-1 grid grid-cols-2 col-span-2 gap-2 -mt-2">
            <CameraView
                class="my-2 border-2 rounded-xl w-full aspect-square col-start-1"
            />
            {#if stimulusType === "dot"}
                <DP class="my-2 border-2 rounded-xl w-full aspect-square col-start-2" pathType="predefined" />
            {:else if stimulusType === "video"}
                <p>
                    Coming soon...
                </p>
            {:else if stimulusType === "file"}
                <DP class="my-2 border-2 rounded-xl w-full aspect-square col-start-2" pathType="file" />
            {/if}
        </div>

        <div class="w-full h-full col-span-2">
            {#if stimulusType === "dot" || stimulusType === "file"}
                <div class="w-full mr-1 p-2 items-center flex">
                    <DotStatistics />
                </div>
            {/if}
        </div>
    </div>
</div>
