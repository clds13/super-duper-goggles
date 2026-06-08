interface DotPath {
    pathCoordinates: { x: number, y: number, coords: number }[];
    pathType: string;
    pathSpeed: number;
    pathJumpFactor: number;
}


function parseDotPathMessage(event: MessageEvent): DotPath {
    const data = event.data.data;
    const pathData = data.pathData;
    const pathCoordinates = data.pathCoordinates;
    const pathType = pathData.type;
    const pathSpeed = pathData.speed;
    const pathJumpFactor = pathData.jumpFactor;

    return {
        pathCoordinates: pathCoordinates,
        pathType: pathType,
        pathSpeed: pathSpeed,
        pathJumpFactor: pathJumpFactor
    }
}

export { parseDotPathMessage };