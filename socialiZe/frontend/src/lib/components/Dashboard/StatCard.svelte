<script lang="ts">
    import Icon from "@iconify/svelte";

    export let icon: string = "";
    export let iconSize: string = "w-full h-full";
    export let title: string = "";
    export let value: string = "";
</script>

<div class="flex flex-col justify-center items-center {$$props.class}">
    <div class="badge-icon variant-filled aspect-square w-full h-full">
        <Icon icon={icon} class="{iconSize}" />
    </div>
    <p class="text-center text-sm">{title}</p>
    <p class="text-center text-sm">{value}</p>
</div>