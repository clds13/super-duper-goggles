import { writable } from "svelte/store";

export const dotColour = writable("red");
export const dotRadius = writable(10);
export const dotPosition = writable({ x: 0, y: 0 });
export const dotAngle = writable(0);