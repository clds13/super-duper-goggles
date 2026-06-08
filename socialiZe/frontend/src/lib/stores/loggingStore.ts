import { writable } from "svelte/store";

export const positionData = writable({
    x: 0,
    y: 0,
    angle: 0,
    timestamp: 0
});