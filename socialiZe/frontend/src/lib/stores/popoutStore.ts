import { writable } from 'svelte/store';

// Create a store for the popout window
export const popoutWindow = writable<Window | null>(null);