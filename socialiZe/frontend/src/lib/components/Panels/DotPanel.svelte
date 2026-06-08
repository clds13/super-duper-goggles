<script lang="ts">
    import Icon from "@iconify/svelte";
    import DS from "$lib/components/Setup/DS.svelte";
    import PS from "$lib/components/Setup/PS.svelte";
    import RS from "$lib/components/Setup/RS.svelte";
</script>

<!-- Configure Dot Stimulus -->
<div class="flex flex-col items-center w-full p-4">
    <!-- Title -->
    <div class="flex flex-row items-center w-full mb-2">
        <Icon icon="lets-icons:bubble" class="w-6 h-6" />
        <h2 class="text-md font-semibold ml-2">Dot Configuration</h2>
    </div>

    <!-- Divider -->
    <hr class="!border-dotted !border-t-2 !w-full my-2" />

    <!-- Component -->
    <DS />
</div>

<hr class="!border-dashed !border-t-2 !w-full" />

<div class="flex flex-col items-center w-full p-4">
    <!-- Title -->
    <div class="flex flex-row items-center w-full mb-2">
        <Icon icon="iconoir:path-arrow" class="w-6 h-6" />
        <h2 class="text-md font-semibold ml-2">Path Configuration</h2>
    </div>

    <!-- Divider -->
    <hr class="!border-dotted !border-t-2 !w-full my-2" />

    <!-- Component -->
    <PS />
</div>

<hr class="!border-dashed !border-t-2 !w-full" />

<div class="flex flex-col items-center w-full p-4">
    <!-- Title -->
    <div class="flex flex-row items-center w-full mb-2">
        <Icon icon="mdi:record-rec" class="w-6 h-6" />
        <h2 class="text-md font-semibold ml-2">Recording Configuration</h2>
    </div>

    <!-- Divider -->
    <hr class="!border-dotted !border-t-2 !w-full my-2" />

    <!-- Component -->
    <RS windowType="predefined" />
</div>
