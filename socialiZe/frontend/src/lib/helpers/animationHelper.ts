/**
     * Scales the data point based on the video resolution. This is necessary to
     * ensure the data point is drawn in the correct position on the canvas.
     *
     * @input dataPoint - The data point to scale
     * @input pathType - The type of path being used
     * @input videoDimensions - The dimensions of the video
     * @input svgWidth - The width of the SVG element
     * @input svgHeight - The height of the SVG element
     * @returns The scaled data point
     */
function scaleData(dataPoint: { x: number; y: number; frame: number }, pathType: string, videoDimensions: { width: number, height: number }, svgWidth: number, svgHeight: number): {
    x: number;
    y: number;
} {

    const radius = Math.min(svgWidth, svgHeight) / 2;
    const centerX = svgWidth / 2;
    const centerY = svgHeight / 2;

    if (pathType === "file") {
        const x = (dataPoint.x / videoDimensions.width) * svgWidth;
        const y = (dataPoint.y / videoDimensions.height) * svgHeight;
        return { x, y };
    } else {
        // Assuming the original Lissajous path was generated with a range of -100 to 100

        // Scale the data point to 50% of the radius of the circle, maintaining the aspect ratio
        const scale = (radius / 2) / 100; // 100 is half of the originalRange
        const x = centerX + dataPoint.x * scale;
        const y = centerY + dataPoint.y * scale;

        return { x, y };
    }
}


/**
 * Animates the SVG element by moving the dot to the next data point in the currentRows array.
 *
 * @input currentRow - The current row of data to animate
 * @input pathType - The type of path being used
 * @input videoDimensions - The dimensions of the video
 * @input svgWidth - The width of the SVG element
 * @input svgHeight - The height of the SVG element
 * @input dotElement - The dot element to animate
 * @returns void
 */
function animateSvg(currentRow: { x: number; y: number, frame: number }, pathType: string, videoDimensions: { width: number, height: number }, svgWidth: number, svgHeight: number, dotElement: SVGCircleElement): void {
    const scaledData = scaleData(currentRow, pathType, videoDimensions, svgWidth, svgHeight);
    dotElement.setAttribute("cx", scaledData.x.toString());
    dotElement.setAttribute("cy", scaledData.y.toString());
}

export { animateSvg, scaleData };