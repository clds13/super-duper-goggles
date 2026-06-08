import { writable, type Writable } from 'svelte/store';


export interface Dot {
    colour: string;
    opacity: number;
    radius: number | undefined;
    fromFile?: boolean;
    filename?: string | undefined;
}


export interface Video {
    videoFile: string;
    duration: number;
}


export const stimulus: Writable<Dot | Video> = writable(
    {
        colour: "#000000",
        opacity: 1,
        radius: undefined,
        fromFile: false,
        filename: undefined,
    }
);


export const trial = writable({
    stimulus: stimulus,
    recordingName: "",
    recordingDuration: 0,
})