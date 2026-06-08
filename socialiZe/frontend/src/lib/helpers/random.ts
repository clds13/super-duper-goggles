/**
 * Returns a seeded random number generator function.
 * 
 * @param seed The seed to use for the random number generator.
 * @returns A seeded random number generator function.
 */
export function SeededRandom(seed: number) {
    var m = 0x80000000;
    var a = 1103515245;
    var c = 12345;

    seed = seed ? seed : Math.floor(Math.random() * m);
    return function() {
        seed = (a * seed + c) % m;
        return seed / m;
    };
}