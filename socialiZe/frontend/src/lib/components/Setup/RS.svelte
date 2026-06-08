<script lang="ts">
    import { writable, type Writable } from "svelte/store";
    import { onMount } from "svelte";
    import { worker } from "$lib/helpers/js/sharedWorker";
    import type { RecordingProperties } from "$lib/types/parameters";

    let recordingName: Writable<string> = writable("");

    // Popout-related
    let popoutWindow: Window | null = null;

    const recordingProperties: Writable<RecordingProperties> = writable({
        duration: 0,
        adaptationDuration: 0,
        fadeInDuration: 0,
        recordingName: "",
        recordingDirectory: "",
        names: {
            project: "",
            experimenter: "",
            description: "",
        }
    });

    export let windowType: "dot" | "predefined" | "video" | "file" = "predefined";
    export let videoFilename: string = "/uploads/video.mp4";

    const buttonText: string[] = [
        `Open Popout (${windowType})`,
        `Start Recording`,
        `Stop Recording`,
    ]
    const buttonTextIndex: Writable<number> = writable(0);

    function openStimulusPopoutWindow() {
        // Open the popout window
        popoutWindow = window.open(
            `/popout/${windowType}`,
            "popout",
            "width=500,height=500"
        );

        if (!popoutWindow) {
            console.error("Failed to open popout window");
            return;
        }

        // Set the popout window to be on top of the main window
        popoutWindow.focus();

        worker.port.postMessage({
            type: "SET_RECORDING_PROPERTIES",
            data: {
                duration: $recordingProperties.duration,
                adaptationDuration: $recordingProperties.adaptationDuration,
                fadeInDuration: $recordingProperties.fadeInDuration,
                recordingName: $recordingProperties.recordingName,
                recordingDirectory: $recordingProperties.recordingDirectory,
                names: $recordingProperties.names,
            }
        });
    }

    onMount(() => {
        if (typeof window !== 'undefined') {
            worker.port.start();
            worker.port.postMessage({ type: "READY" });
            
            worker.port.addEventListener("message", (event: MessageEvent) => {
                if (event.data.type === "RECORDING_PROPERTIES") {
                    console.log("Received recording properties from worker");
                    console.log(event.data.data);
                }
            });
        }
    });
</script>

<div
    class="flex flex-col w-full rounded-xl items-center {$$props.class}"
>
    <!-- Settings -->
    <div class="flex flex-col py-2 justify-center w-full">

        <div class="flex flex-col my-2">
            <label for="recordingDuration">Recording Duration (seconds):</label>
            <input
                id="recordingDuration"
                type="number"
                class="input"
                bind:value={$recordingProperties.duration}
                min="0"
            />
        </div>
        
        <div class="flex flex-col my-2">
            <label for="adaptationDuration">Adaptation Duration (seconds):</label>
            <input
                id="adaptationDuration"
                type="number"
                class="input"
                bind:value={$recordingProperties.adaptationDuration}
                min="0"
            />
        </div>

        <div class="flex flex-col my-2">
            <label for="stimulusDelay">Stimulus Delay (seconds):</label>
            <input
                id="stimulusDelay"
                type="number"
                class="input"
                bind:value={$recordingProperties.fadeInDuration}
                min="0"
            />
        </div>

        <div class="flex flex-col my-2">
            <label for="projectName">Project Name:</label>
            <input
                id="projectName"
                type="text"
                class="input"
                bind:value={$recordingProperties.names.project}
            />
        </div>

        <div class="flex flex-col my-2">
            <label for="experimenterName">Experimenter Name:</label>
            <input
                id="experimenterName"
                type="text"
                class="input"
                bind:value={$recordingProperties.names.experimenter}
            />
        </div>

        <div class="flex flex-col my-2">
            <label for="description">Short Description:</label>
            <input
                id="description"
                type="text"
                class="input"
                bind:value={$recordingProperties.names.description}
            />
        </div>

        <!-- <div class="flex flex-col my-2">
            <label for="recordingName">Recording Name:</label>
            <input
                id="recordingName"
                type="text"
                class="input"
                bind:value={$recordingProperties.recordingName}
                disabled
            />
        </div> -->

        <!-- <div class="flex flex-col my-2">
            <label for="recordingsDir">Recordings Directory:</label>
            <input
                id="recordingsDir"
                type="text"
                class="input"
                bind:value={$recordingProperties.recordingDirectory}
                disabled
            />
        </div> -->

    </div>

    <!-- Buttons -->
    <div class="flex flex-col px-4 pb-2 justify-center w-full">
        <button
            type="button"
            class="btn bg-primary-500 w-full mt-2"
            on:click={openStimulusPopoutWindow}
            >{buttonText[$buttonTextIndex]}</button
        >
    </div>
</div>
