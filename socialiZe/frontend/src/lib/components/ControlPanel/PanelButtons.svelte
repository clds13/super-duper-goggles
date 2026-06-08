<script lang="ts">
    import { arenaWidth, arenaHeight, arenaColour } from "$lib/stores/arenaStore";
    // import { dotColour, dotRadius, dotPosition, dotAngle } from "$lib/stores/dotStore";
    // import { circularRadius, circularSpeed, circularDirection } from "$lib/stores/circularPathStore";
    import { activeViews } from "$lib/stores/statusStore";
    import { positionData } from "$lib/stores/loggingStore";
    import { dotProperties } from "$lib/stores/dotTestStore";
    import { popoutWindow } from "$lib/stores/popoutStore";
    

    let messageListenerAdded = false;

    // Button handlers
    const popout = () => {
        console.log("Popout");

        // Collect the params from the stores
        const params = new URLSearchParams({
            arenaWidth: $arenaWidth.toString(),
            arenaHeight: $arenaHeight.toString(),
            arenaColour: $arenaColour,
            dotColour: $dotProperties.colour,
            dotRadius: $dotProperties.radius.toString(),
            dotPosition: JSON.stringify($dotProperties.position),
            dotAngle: $dotProperties.angle.toString(),
            circularRadius: $dotProperties.path.radius.toString(),
            circularSpeed: $dotProperties.path.speed.toString(),
            circularDirection: $dotProperties.path.direction,
        });

        // Open the /popout/circular page in a new window
        popoutWindow.set(window.open(`/popout/fish?${params.toString()}`, "_blank", "width=500,height=500"));

        if (popoutWindow) {
            console.log("Popout window opened");

            setTimeout(() => {
                console.log("Sending INIT message to popout window");
                if ($popoutWindow) {
                    $popoutWindow.postMessage({
                        type: 'INIT',
                        properties: $dotProperties
                    });
                } else {
                    console.log("Popout window is null");
                }
            }, 1000);

            // Set an interval to check if the popout window is closed
            const checkPopout = setInterval(() => {
                if ($popoutWindow) {
                    if ($popoutWindow.closed) {
                        clearInterval(checkPopout);
                        console.log("Popout window is closed");
                    }
                } else {
                    console.log("Popout window is null");
                }
            }, 500);

            if (!messageListenerAdded) {
                window.addEventListener('message', (event) => {
                    if (event.data.type === 'positionData') {
                        const positionData = event.data.content;
                        console.log('Received position data:', positionData);

                        // Combine position data with metadata
                        // TODO: Make pathSeed dynamic and not hardcoded.
                        const combinedData = JSON.stringify({
                            positionData: positionData,
                            params: {
                                arenaWidth: $arenaWidth,
                                arenaHeight: $arenaHeight,
                                arenaColour: $arenaColour,
                                dotColour: $dotProperties.colour,
                                dotRadius: $dotProperties.radius,
                                dotPosition: JSON.stringify($dotProperties.position),
                                dotAngle: $dotProperties.angle,
                                pathRadius: $dotProperties.path.radius,
                                pathSpeed: $dotProperties.path.speed,
                                pathDirection: $dotProperties.path.direction,
                                pathSeed: 1234
                            }
                        });
                        
                        // Save the position data to the store
                        $positionData = positionData;

                        // Create a Blob from the data
                        const fileToSave = new Blob([combinedData], { type: 'application/json' });

                        // Create a URL for the Blob
                        const fileURL = URL.createObjectURL(fileToSave);

                        // Create an anchor element and set attributes for download
                        const downloadLink = document.createElement('a');
                        downloadLink.href = fileURL;
                        downloadLink.download = 'positionData.json'; // Set the file name

                        // Append the link to the document and trigger the download
                        document.body.appendChild(downloadLink);
                        downloadLink.click();

                        // Clean up
                        document.body.removeChild(downloadLink);
                        URL.revokeObjectURL(fileURL);
                    }
                });

                messageListenerAdded = true;
            }
        } else {
            console.log("Popout window blocked");
        }
    }

    const preview = () => {

        // Check if the preview is already open
        if ($activeViews.includes("Preview")) {
            // Close the preview
            $activeViews = $activeViews.filter((view) => view !== "Preview");
            return;
        }

        $activeViews = [...$activeViews, "Preview"];
    }

    const camera = () => {

        // Check if the camera is already open
        if ($activeViews.includes("Camera")) {
            // Close the camera
            $activeViews = $activeViews.filter((view) => view !== "Camera");
            return;
        }

        $activeViews = [...$activeViews, "Camera"];
    }

</script>


<div class="w-full flex flex-row">
    <!-- Popout Button -->
    <button type="button" class="btn variant-filled w-full" on:click={popout}>
        Popout
    </button>

    {#if $activeViews.includes("Preview")}
        <button type="button" on:click={preview} class="btn variant-filled-primary w-full mx-2">
            Preview
        </button>
    {:else}
        <button type="button" on:click={preview} class="btn variant-filled w-full mx-2">
            Preview
        </button>
    {/if}

    <!-- Highlight Camera if it is the active view -->
    {#if $activeViews.includes("Camera")}
        <button type="button" on:click={camera} class="btn variant-filled-primary w-full variant">
            Camera
        </button>
    {:else}
        <button type="button" on:click={camera} class="btn variant-filled w-full">
            Camera
        </button>
    {/if}
</div>
