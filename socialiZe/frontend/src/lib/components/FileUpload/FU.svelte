<script lang="ts">
    import Icon from "@iconify/svelte";
    import { type Writable, writable } from "svelte/store";
    import { onMount } from "svelte";
    import * as Papa from "papaparse";
    import { worker } from "$lib/helpers/js/sharedWorker";

    const fileUploadDragged: Writable<boolean> = writable(false);

    const fileUploaded: Writable<boolean> = writable(false);
    const fileUploadText: Writable<string> = writable(
        "Drag and drop a file here or click to upload.",
    );
    const filename: Writable<string> = writable("");
    const filesize: Writable<number> = writable(0);
    const filelines: Writable<number> = writable(0);    

    onMount(() => {
        console.log("FileUpload component mounted");
        if (typeof window !== "undefined") {
            worker.port.start();
            worker.port.postMessage({ type: "READY" });
            worker.port.postMessage({ type: "RESET" });

            // Post a reset message to the worker
            // worker.port.postMessage({
            //     type: "RESET",
            // });

            // worker.port.addEventListener('message', (event: MessageEvent) => {
            //     if (event.data.type === "CSV_INFO") {
            //         const { name, size, lines } = event.data.data;
            //         console.log(name, size, lines);
            //         $filename = name;
            //         $filesize = size;
            //         $filelines = lines;
            //         $fileUploaded = true;
            //     }
            // });
        }
    });

    $: if ($fileUploaded) {
        $fileUploadText = "File uploaded!";
    } else {
        $fileUploadText = "Drag and drop a file here or click to upload.";
    }

    const processFile = (file: File) => {
        Papa.parse(file, {
            header: true,
            complete: (results) => {
                const data = results.data as Array<{ x: string | number; y: string | number; coords: string | number }>;
                const processedData = data.map((entry) => {
                    if (entry.x === '') {
                        entry.x = 0;
                    }
                    if (entry.y === '') {
                        entry.y = 0;
                    }

                    // Check for any NaN values and replace them with 0
                    if (isNaN(entry.x as number)) {
                        entry.x = 0;
                    }
                    if (isNaN(entry.y as number)) {
                        entry.y = 0;
                    }

                    // Convert x and y to numbers
                    entry.x = +entry.x;
                    entry.y = +entry.y;

                    // Convert coords to numbers
                    entry.coords = +entry.coords;

                    return entry;
                });

                worker.port.postMessage({
                    type: "SET_DOT_PATH",
                    data: {
                        pathType: "file",
                        pathData: {
                            fileData: {
                                name: file.name,
                                size: file.size,
                                lines: processedData.length,
                            },
                            pathCoordinates: processedData
                        }
                    }
                })
                $filename = file.name;
                $filesize = file.size;
                $filelines = processedData.length;
                $fileUploaded = true;
            }
        })
    }

    const resetFileUpload = () => {
        $fileUploaded = false;
        $filename = "";
        $filesize = 0;
        $filelines = 0;
    };

    const handleInputChange = (event: Event) => {
        const input = event.target as HTMLInputElement;
        if (input && input.files && input.files.length > 0) {
            const file = input.files?.[0];
            processFile(file);
        } else {
            resetFileUpload();
        }
    };
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
            processFile(file);
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
                    on:click|preventDefault={resetFileUpload}
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
            <input type="file" class="hidden" on:change={handleInputChange} />
        </div>
    {/if}
</label>
