import { writable } from "svelte/store";

export const arenaWidth = writable(100);
export const arenaHeight = writable(100);
export const arenaColour = writable("white");