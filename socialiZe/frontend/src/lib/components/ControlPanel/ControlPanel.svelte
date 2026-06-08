<script>
    import ArenaControls from "./ArenaControls.svelte";
    import DotControls from "./DotControls.svelte";
    import PathControls from "./PathControls.svelte";
    import PanelButtons from "./PanelButtons.svelte";
    import RecordingButtons from "./RecordingButtons.svelte";
</script>

<div class="w-full {$$props.class}">

    <DotControls />

    <!-- Divider -->
    <hr class="!border-t-4 !border-dotted my-2" />

    <ArenaControls />

    <!-- Divider -->
    <hr class="!border-t-4 !border-dotted my-2" />

    <PathControls />

    <!-- Divder -->
    <hr class="!border-t-4 !border-dotted my-2" />

    <PanelButtons />

    <!-- Divider -->
    <hr class="!border-t-4 !border-dotted my-2" />

    <RecordingButtons />
</div>