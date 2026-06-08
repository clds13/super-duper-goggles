<script lang="ts">
    import Icon from "@iconify/svelte";
    import { onMount } from "svelte";
    import { type Writable, writable } from "svelte/store";

    // Stores
    let invisible: Writable<boolean> = writable(false);
    let duration: Writable<number> = writable(0);
    export let filename: string | null = "";
    let remainingTime: Writable<number> = writable(0);    

    /**
     * Closes the current window and sends the position data to the opener
     * window. If the opener window is closed or doesn't exist, the function
     * does nothing.
     *
     * @returns {void}
     */
    function closeWindow(): void {
        // Close the current window
        window.close();
    }

    onMount(() => {
        // Add the Tailwind CSS styles to the head of the document
        const link = document.createElement("link");
        link.rel = "stylesheet";
        link.href = "../src/app.postcss";
        document.head.appendChild(link);

        // 
        console.log("🚀 ~ file: VideoPopout.svelte:10 ~ filename:", filename)

        

        window.addEventListener("message", (event) => {
            if (event.data.type === "START_REC") {
                // Set the recording duration
                const duration = event.data.duration;
                $duration = duration;

                // Set the recording filename
                // const recFilename = event.data.filename;
                // console.log(recFilename);
                // filename = recFilename;
            }
        });
    });

    function onKeydown(event: { key: string }) {
        if (event.key === "q") {
            closeWindow();
        } else if (event.key === "h") {
            $invisible = !$invisible;
        }
    }
</script>

<svelte:window on:keydown={onKeydown} />

<div class="flex items-center justify-center {$$props.class}">
    <!-- Control Buttons -->
    <div class="fixed top-0 left-0 m-1 z-10 flex">
        <!-- Close Button -->
        <button class="btn variant-filled-primary p-1" on:click={closeWindow}>
            <Icon icon="material-symbols:close-rounded" class="w-6 h-6" />
        </button>
        <!-- Help/Info Icon -->
        <button
            class="btn variant-filled-secondary p-1 ml-2"
            title="Keybinds: 'q' to close, 'r' to reset, 'h' to toggle visibility"
        >
            <Icon
                icon="material-symbols:help-outline-rounded"
                class="w-6 h-6"
            />
        </button>
    </div>

    <!-- Video -->
    <div class="border rounded-full w-screen h-screen z-10 border-red-500">
        <div class="w-full h-full relative -z-10">
            <video
                class="w-full h-full -z-10 object-cover rounded-full"
                autoplay
                muted
                loop
                width="100%"
                src={`http://localhost:8000/uploads/${filename}`}
            >

            </video>
        </div>
    </div>

    <!-- Top Right Text -->
    <div class="fixed top-0 right-0 m-1 z-50 flex">
        <div class="flex flex-col">
            <!-- <div class="flex flex-row">
                <p class="text-white text-sm font-bold">{$filename}</p>
            </div> -->
            <div class="flex flex-row">
                <p class="text-white text-sm font-bold">{$remainingTime} s</p>
            </div>
        </div>
    </div>
</div>
