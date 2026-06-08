<script lang="ts">
    import { dotColour, dotRadius } from "$lib/stores/dotStore";
    import { dotProperties } from "$lib/stores/dotTestStore";

    
    // $: $dotColour = $dotColour;
    // $: $dotRadius = $dotRadius;
</script>


<div class="w-full">
    <!-- Dot Colour (Alphabetical) -->
    <div class="flex flex-col my-2">
        <label for="dotColour">Dot Colour</label>
        <select name="dotColour" id="dotColour" class="select" bind:value={$dotProperties.colour}>
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

    <!-- Dot Radius -->
    <div class="flex flex-col my-2">
        <label for="dotRadius">Dot Radius</label>
        <input type="range" name="dotRadius" id="dotRadius" min="10" max="100"  class="slider" bind:value={$dotProperties.radius}>
    </div>
</div>