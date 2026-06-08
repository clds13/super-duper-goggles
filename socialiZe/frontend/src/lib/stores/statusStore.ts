import { writable } from "svelte/store";

export const activeViews = writable(["Preview", "Camera"]);
export const recordingStatus = writable("stopped");