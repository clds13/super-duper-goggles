<script lang="ts">
    import { arenaWidth, arenaHeight, arenaColour } from '$lib/stores/arenaStore';

    
    $: $arenaWidth = $arenaWidth;
    $: $arenaHeight = $arenaHeight;
    $: $arenaColour = $arenaColour;
</script>


<div class="w-full">
    <!-- Arena Width -->
    <div class="flex flex-col my-2">
        <label for="arenaWidth">Arena Width</label>
        <input type="range" name="arenaWidth" id="arenaWidth" min="10" max="100"  class="slider" bind:value={$arenaWidth}>
    </div>

    <!-- Arena Height -->
    <div class="flex flex-col my-2">
        <label for="arenaHeight">Arena Height</label>
        <input type="range" name="arenaHeight" id="arenaHeight" min="10" max="100"  class="slider" bind:value={$arenaHeight}>
    </div>

    <!-- Arena Colour (Alphabetical) -->
    <div class="flex flex-col my-2">
        <label for="arenaColour">Arena Colour</label>
        <select name="arenaColour" id="arenaColour" class="select" bind:value={$arenaColour}>
            <option value="black">Black</option>
            <option value="blue">Blue</option>
            <option value="green">Green</option>
            <option value="orange">Orange</option>
            <option value="purple">Purple</option>
            <option value="red">Red</option>
            <option value="white">White</option>
            <option value="yellow">Yellow</option>
        </select>
    </div>
</div>