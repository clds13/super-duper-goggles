<script lang="ts">
    import { page } from "$app/stores";
    import VideoPopout from "$lib/components/Popout/VideoPopout.svelte";
    import { onMount } from "svelte";
    import { writable, type Writable } from "svelte/store";

    const showLines = writable(false);

    // const filename = $page.url.searchParams.get("filename");
    const filename: Writable<string | null> = writable($page.url.searchParams.get("filename"));

    onMount(() => {
        console.log("Mounted");
        console.log($filename);
    });

    $: console.log($showLines);
</script>

<div
    class="w-screen h-screen relative"
    on:click={() => ($showLines = !$showLines)}
    on:keydown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
            $showLines = !$showLines;
        }
    }}
    tabindex="0"
    role="button"
    aria-label="Toggle visibility of lines"
>
    {#if $showLines}
        <div class="line top" style="top: 0;"></div>
        <div class="line bottom" style="bottom: 0;"></div>
        <div class="line left" style="left: 0;"></div>
        <div class="line right" style="right: 0;"></div>
    {/if}

    <VideoPopout filename={$filename} />
</div>

<style>
    .line {
        position: absolute;
        background-color: white;
        width: 15px;
        height: 20px;
    }

    .top,
    .bottom {
        left: 50%;
    }

    .left,
    .right {
        top: 50%;
    }

    .top {
        transform: translateX(-50%);
        background-color: red;
        z-index: -1;
    }

    .bottom {
        transform: translate(-50%, -1px);
    }

    .left {
        transform: translateY(-50%) translateX(0) rotate(90deg);
    }

    .right {
        transform: translate(-1px, -50%) translateX(0) rotate(90deg);
        background-color: blue;
        z-index: -1;
    }
</style>
