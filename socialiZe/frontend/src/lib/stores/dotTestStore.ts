import { writable } from 'svelte/store';

export const dotProperties = writable(
    {
        colour: "#000000",
        opacity: 1,
        radius: 10,
        position: { x: 0, y: 0 },
        angle: 0,
        path: {
            type: "fish",
            radius: 0.5,
            speed: 0.01,
            direction: "clockwise",
        },
        test: {
            filename: "",
            duration: 0,
            destination: "",
            arenaRadius: 1,
            speed: 0.01,
            history: false
        }
    }
);