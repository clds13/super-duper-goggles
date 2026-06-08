interface Coordinate {
    x: number;
    y: number;
}


/**
 * Calculates the total distance between a series of coordinates.
 * 
 * @param coordinates - An array of coordinates.
 * @param conversionFactor - The conversion factor to apply to the coordinates.
 * @returns The total distance between the coordinates.
 */
function calculateTotalDistance(coordinates: Coordinate[], conversionFactor: number = 1): number {
    let totalDistance: number = 0;
    for (let i = 1; i < coordinates.length; i++) {
        const dx: number = coordinates[i].x - coordinates[i - 1].x;
        const dy: number = coordinates[i].y - coordinates[i - 1].y;
        const distance: number = Math.sqrt(dx * dx + dy * dy) * conversionFactor;
        totalDistance += distance;
    }
    return totalDistance;
}

export { calculateTotalDistance };