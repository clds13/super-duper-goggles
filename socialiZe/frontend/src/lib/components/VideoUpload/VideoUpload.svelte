<script lang="ts">
    import Icon from "@iconify/svelte";
    import { type Writable, writable } from "svelte/store";
    import { handleFileUpload } from "$lib/utils/handleInputUpload";

    const fileUploadDragged: Writable<boolean> = writable(false);

    const fileUploaded: Writable<boolean> = writable(false);
    const fileUploadText: Writable<string> = writable(
        "Drag and drop a video here or click to upload.",
    );
    const filename: Writable<string> = writable("");
    const filesize: Writable<number> = writable(0);
    const filelines: Writable<number> = writable(0);

    $: if ($fileUploaded) {
        $fileUploadText = "File uploaded!";
    } else {
        $fileUploadText = "Drag and drop a file here or click to upload.";
    }

    const handleInputChange = (event: Event) => {
        const input = event.target as HTMLInputElement;
        if (input && input.files) {
            const file = input.files[0];
            if (file) {
                handleFileUpload(file).then((data) => {
                    $filename = data.filename;
                    $filesize = data.filesize;
                    $filelines = data.numLines;
                });
                $fileUploaded = true;
            }
        }
    }
</script>

<label
    class="{$fileUploadDragged
        ? 'bg-gray-800'
        : ''} flex flex-col items-center justify-center h-64 w-full border-2 border-dashed border-gray-400 rounded-xl hover:cursor-pointer hover:bg-gray-800"
    on:dragover={(event) => {
        event.preventDefault();
        $fileUploadDragged = true;
    }}
    on:drop={(event) => {
        event.preventDefault();
        const file = event.dataTransfer?.files[0];
        if (file) {
            handleFileUpload(file).then((data) => {
                $filename = data.filename;
                $filesize = data.filesize;
                $filelines = data.numLines;
            });
            $fileUploaded = true;
        }
    }}
    on:dragleave={(event) => {
        event.preventDefault();
        $fileUploadDragged = false;
    }}
>
    {#if $fileUploaded}
        <div class="flex flex-col items-center justify-center space-y-2 m-2">
            <Icon icon="mdi:file" class="w-12 h-12" />
            <div class="flex flex-col items-center justify-center space-y-2">
                {#if $filename}
                    <p class="text-gray-400">
                        {$filename.split("/").pop()}
                    </p>
                {/if}
                {#if $filesize}
                    <p class="text-gray-400">
                        {new Intl.NumberFormat("en-US", {
                            style: "decimal",
                        }).format($filesize / 1024 / 1024)}{" "}
                        MB
                    </p>
                {/if}
                {#if $filelines}
                    <p class="text-gray-400">
                        {new Intl.NumberFormat("en-US", {
                            style: "decimal",
                        }).format($filelines)}{" "}
                        lines
                    </p>
                {/if}
            </div>
            <div class="flex flex-row w-full space-x-2">
                <button
                    class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded w-full mb-2"
                >
                    Reset
                </button>
            </div>
        </div>
    {:else}
        <div class="flex flex-col items-center justify-center space-y-2">
            <Icon icon="mdi:file" class="w-12 h-12" />
            {#if $fileUploadText}
                <p class="text-gray-400">
                    {$fileUploadText}
                </p>
            {:else}
                <p class="text-gray-400">
                    {$fileUploadText}
                </p>
            {/if}
            <input
                type="file"
                class="hidden"
                on:change={handleInputChange}
            />
        </div>
    {/if}
</label>
