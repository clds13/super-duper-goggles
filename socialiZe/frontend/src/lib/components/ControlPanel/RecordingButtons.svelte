<script lang="ts">
    import { recordingStatus } from "$lib/stores/statusStore";
    

    // Button handlers
    const record = () => {
        console.log("Record");

        // Change recording status
        if ($recordingStatus === "recording") {
            $recordingStatus = "stopped";
        } else {
            $recordingStatus = "recording";
        }
    }

</script>


<div class="w-full flex flex-row">
    <!-- Popout Button -->
    <button type="button" class="btn variant-filled w-full" on:click={record}>
        {#if $recordingStatus === "recording"}
            Stop Recording
        {:else}
            Start Recording
        {/if}
    </button>
</div>
