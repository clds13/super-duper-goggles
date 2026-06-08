const svgNS = "http://www.w3.org/2000/svg";

export function initializeDot(svgElement: SVGSVGElement): Element {
    let dotElement: SVGCircleElement = document.createElementNS(svgNS, "circle");
    svgElement.appendChild(dotElement);

    return dotElement;
}


export function initializeSvg(svgElement: SVGSVGElement): Element {
    let svgWidth = svgElement.clientWidth;
    let svgHeight = svgElement.clientHeight;
    let dotElement = document.createElementNS(svgNS, "circle");
    svgElement.appendChild(dotElement);
    return dotElement;
}

// NOTE: This one lets the dot fade in. Use `initializeDot` first, then `initializeSvg2` to fade in the dot.
export function initializeSvg2(dotElement: SVGCircleElement, transitionDuration: number): SVGCircleElement {
    dotElement.style.transition = `opacity ${transitionDuration}s`;
    dotElement.setAttribute("opacity", "0");

    return dotElement;
}

export function setDotProperties(dotElement: SVGCircleElement, size: number, colour: string, opacity: number): void {
    dotElement.setAttribute("r", size.toString());
    dotElement.setAttribute("fill", colour);
    dotElement.setAttribute("opacity", opacity.toString());
}