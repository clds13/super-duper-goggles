<script lang="ts">
    import { onMount } from "svelte";
    import { recordingStatus } from "$lib/stores/statusStore";
    import { popoutWindow } from "$lib/stores/popoutStore";
    import { dotProperties } from "$lib/stores/dotTestStore";

    let videoStreamUrl: string = "";
    let ws: WebSocket;

    /**
     * Establishes a WebSocket connection and sets up event listeners.
     */
    function setupWebSocket() {
        ws = new WebSocket("ws://localhost:8000/ws/camera-feed");

        ws.onopen = () => {
            console.log("WebSocket connection established");
        };

        ws.onmessage = (event) => {
            if (event.data instanceof Blob) {
                handleBlobMessage(event.data);
            } else {
                handleOtherMessage(event.data);
            }
        };

        ws.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        ws.onclose = () => {
            console.log("WebSocket connection closed");
        };
    }

    /**
     * Handles Blob messages received from the WebSocket.
     * @param {Blob} data - The Blob data received from the WebSocket.
     */
    function handleBlobMessage(data: Blob) {
        if (videoStreamUrl) {
            URL.revokeObjectURL(videoStreamUrl);
        }
        videoStreamUrl = URL.createObjectURL(data);
    }

    /**
     * Handles other messages received from the WebSocket.
     * @param {string} data - The message data received from the WebSocket.
     */
    function handleOtherMessage(data: string) {
        console.log("Received message:", data);
    }

    /**
     * Closes the WebSocket connection and cleans up resources.
     */
    function cleanupWebSocket() {
        ws.close();
        if (videoStreamUrl) {
            URL.revokeObjectURL(videoStreamUrl);
        }
    }

    /**
     * Sends a start message to the backend when recordingStatus is set to "recording".
     */
    function sendStartMessage() {
        if (ws && ws.readyState === WebSocket.OPEN) {
            let filename: string = $dotProperties.test.filename;
            let duration: number = $dotProperties.test.duration;
            let destination: string = $dotProperties.test.destination;

            ws.send(JSON.stringify({ command: "start", filename: filename, duration: duration, destination: destination }));

            // Post a message to the popout window of the filename and duration
            // if ($popoutWindow) {
            //     $popoutWindow.postMessage({
            //         type: "START_REC",
            //         filename: filename,
            //         duration: duration,
            //     });
            // }
        } else {
            console.error("WebSocket is not open. Try running the backend using `uvicorn main:app --reload`.");
        }
    }

    /**
     * Sends a stop message to the backend when recordingStatus is set to "stopped".
     */
    function sendStopMessage() {
        if (ws && ws.readyState === WebSocket.OPEN) {
            console.log("Sending 'stop' message");
            ws.send(JSON.stringify({ command: "stop" }));
        }
    }

    onMount(() => {
        setupWebSocket();
        // Cleanup function when the component is unmounted
        return cleanupWebSocket;
    });

    $: {
        if ($recordingStatus === "recording") {
            sendStartMessage();
        } else if ($recordingStatus === "stopped") {
            sendStopMessage();
        }
    }
</script>

<div class="w-full h-auto flex items-center justify-center {$$props.class}">
    <img src={videoStreamUrl} alt="Live Video Feed" />
</div>

<style>
    .video-container {
        width: 100%;
        height: auto;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    img {
        max-width: 100%;
        height: auto;
    }
</style>
