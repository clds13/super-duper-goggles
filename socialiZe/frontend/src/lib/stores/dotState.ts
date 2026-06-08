import { writable, type Writable } from "svelte/store";

export const isPathReset: Writable<boolean> = writable(false);