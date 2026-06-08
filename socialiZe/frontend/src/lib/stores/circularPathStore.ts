import { writable } from "svelte/store";

export const pathChoice = writable("fish");
export const circularRadius = writable(150);
export const circularSpeed = writable(0.01);
export const circularDirection = writable("clockwise");
