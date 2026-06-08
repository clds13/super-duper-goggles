<script lang="ts">
    // import { pathChoice, circularRadius, circularSpeed, circularDirection } from "$lib/stores/circularPathStore";
    import { dotProperties } from "$lib/stores/dotTestStore";
</script>


<div class="w-full">
    <!-- Path Choice (Alphabetical) -->
    <div class="flex flex-col my-2">
        <label for="pathChoice">Path Choice</label>
        <select name="pathChoice" id="pathChoice" class="select" bind:value={$dotProperties.path.type}>
            <option value="circular">Circular</option>
            <option value="fish">Fish-like</option>
            <option value="linear">Linear</option>
        </select>
    </div>

    <div class="flex flex-col my-2">
        <label for="circularRadius">Circular Radius</label>
        <input type="range" name="circularRadius" id="circularRadius" min="0" max="200"  class="slider" bind:value={$dotProperties.path.radius}>

        <label for="circularAngle">Circular Speed</label>
        <input type="range" name="circularSpeed" id="circularSpeed" min="0.01" max="0.05"  class="slider" bind:value={$dotProperties.path.speed} step="0.005">

        <label for="circularDirection">Circular Direction</label>
        <select name="circularDirection" id="circularDirection" class="select" bind:value={$dotProperties.path.direction}>
            <option value="clockwise">Clockwise</option>
            <option value="counterclockwise">Counterclockwise</option>
        </select>
    </div>

    <!-- Linear isn't implemented yet. -->
</div>