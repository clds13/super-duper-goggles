/**
 * Creates a list of objects with an x and y value that correspond to the
 * path type specified. Path types include 'circular', and 'lissajous'.
 * 
 * @param {string} pt - The type of path to create.
 * @param {number} duration - The duration of the path.
 * @param {number} frameMultiplier - The multiplier for the number of frames.
 * @returns { { x: number, y: number }[] } - The list of objects with x and y values.
 * @see https://en.wikipedia.org/wiki/Lissajous_curve
 * @see https://en.wikipedia.org/wiki/Circular_motion
 */
// function createPath(pt: string, duration: number, frameMultiplier: number = 1): { x: number, y: number, coords: number }[] {
//     const adjustedDuration = duration * frameMultiplier;

//     if (pt === 'circular') {
//         return calculateCircularPath(adjustedDuration);
//     } else if (pt === 'lissajous') {
//         return calculateLissajousPath(adjustedDuration);
//     }

//     return [];
// }
function createPath(pt: string, duration: number, frameMultiplier: number = 1): { x: number, y: number, coords: number }[] {
    let path: { x: number, y: number, coords: number }[];

    if (pt === 'circular') {
        path = calculateCircularPath(duration);
    } else if (pt === 'lissajous') {
        path = calculateLissajousPath(duration);
    } else {
        path = [];
    }

    // Create a new array that keeps every `frameMultiplier`th frame and replaces the frames in-between with the previous frame
    const newPath: { x: number, y: number, coords: number }[] = [];
    let previousFrame: { x: number, y: number, coords: number } | null = null;

    for (let i = 0; i < path.length; i++) {
        if (i % frameMultiplier === 0) {
            newPath.push(path[i]);
            previousFrame = path[i];
        } else if (previousFrame) {
            newPath.push(previousFrame);
        }
    }

    return newPath;
}

/**
 * Helper function to calculate the x and y values of a circular path.
 * 
 * @param {number} duration - The number of steps in the path.
 * @returns { { x: number, y: number }[] } - The list of objects with x and y values.
 */
function calculateCircularPath(duration: number): { x: number, y: number, coords: number }[] {
    const path: { x: number, y: number, coords: number }[] = [];
    const radius = 100;
    const angleStep = (2 * Math.PI) / duration;

    for (let i = 0; i < duration; i++) {
        const x = radius * Math.cos(angleStep * i);
        const y = radius * Math.sin(angleStep * i);
        path.push({ x: x, y: y, coords: i });
    }

    return path;
}

/**
 * Helper function to calculate the x and y values of a path based on a
 * Lissajous curve.
 * 
 * @param {number} duration - The number of steps in the path.
 * @returns { { x: number, y: number }[] } - The list of objects with x and y values.
 */
function calculateLissajousPath(duration: number): { x: number, y: number, coords: number }[] {
    const path: { x: number, y: number, coords: number }[] = [];
    const a = 100;
    const b = 100;
    const delta = Math.PI / 2;
    const angleStep = (2 * Math.PI) / duration;

    for (let i = 0; i < duration; i++) {
        const x = a * Math.sin(3 * angleStep * i + delta);
        const y = b * Math.sin(2 * angleStep * i);
        path.push({ x: x, y: y, coords: i });
    }

    return path;
}

export { createPath };