import random
from js import document, DOMParser, URL, FileReader, console, setTimeout, window
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy
from pyodide.ffi.wrappers import set_interval, clear_interval

svg_mover = None 

class SvgMover:
    def __init__(self, svg_element, interval=100):
        self.svg_element = svg_element
        self.container = document.getElementById('svg-container')
        self.container.innerHTML = ""
        self.container.appendChild(self.svg_element)

        self.paths = self.svg_element.getElementsByTagName("path")

        self.positions = [{'x': 0, 'y': 0} for _ in range(len(self.paths))]
        self.directions = [{'x': random.choice([-1, 1]), 'y': random.choice([-1, 1])} for _ in range(len(self.paths))]

        self.interval = interval
        self.timer = set_interval(self.animate, self.interval)

    def animate(self):
        for i, path in enumerate(self.paths):
            pos = self.positions[i]
            dir = self.directions[i]

            pos['x'] += dir['x'] * random.uniform(0.1, 0.5)
            pos['y'] += dir['y'] * random.uniform(0.1, 0.5)

            if pos['x'] > 40 or pos['x'] < -40:
                dir['x'] *= -1
            if pos['y'] > 40 or pos['y'] < -40:
                dir['y'] *= -1

            path.setAttribute("transform", f"translate({pos['x']}, {pos['y']})")

    def stop(self):
        if hasattr(self, 'timer'):
            clear_interval(self.timer)



def handle_upload(event):
    event.preventDefault()
    file_input = document.getElementById('file-input')
    file = file_input.files.item(0)
    if file:
        file_reader = FileReader.new()
        file_reader.onload = create_proxy(lambda e: load_new_svg(file_reader.result))
        file_reader.readAsText(file)

def load_svg_from_string(svg_string):
    parser = DOMParser.new()
    doc = parser.parseFromString(svg_string, "image/svg+xml")

    if doc.documentElement.tagName != "svg" or doc.documentElement.namespaceURI not in ["http://www.w3.org/2000/svg", "x"]:
        raise ValueError("Root element is not <svg> or has incorrect namespace")

    allowed_elements = [        # 여기에 있는 태그들만 통과, 여기에 없는 태그를 쓰면 ValueError가 발생함
        "svg", "path", "rect", "circle", "ellipse", "line", "polyline", "polygon",
        "text", "tspan", "textPath", "altGlyph", "altGlyphDef", "altGlyphItem",
        "glyphRef", "altGlyph", "animate", "animateColor", "animateMotion",
        "animateTransform", "mpath", "set", "desc", "title", "metadata",
        "defs", "g", "symbol", "use", "image", "switch", "style"
    ]

    elements = doc.getElementsByTagName("*")    # doc 전체에서 사용된 모든 태그들을 다 가져옴
    for element in elements:
        if element.tagName not in allowed_elements: # element의 태그가 허용된 태그들 중에 있는지 확인하고 없으면 true가 돼서 아래 실행
            raise ValueError(f"Disallowed SVG element found: {element.tagName}")

    return doc.documentElement

def load_new_svg(svg_content):
    svg_container = document.getElementById('svg-container')
    original_svg_content = document.getElementById('original-svg-content')

    try:
        svg_element = load_svg_from_string(svg_content)
        if svg_element.tagName != "svg":
            raise ValueError("Not a valid SVG")
    except Exception as e:
        original_svg_content.innerHTML = "Invalid SVG!!"
        svg_container.innerHTML = "Invalid SVG!!"
        console.error(f"Invalid SVG: {e}")
        return

    original_svg_content.innerHTML = svg_content

    svg_element = load_svg_from_string(svg_content)
    svg_container.innerHTML = ""
    svg_container.appendChild(svg_element)

    initialize_svg_mover(svg_content)

def initialize_svg_mover(svg_content):
    global svg_mover
    svg_element = load_svg_from_string(svg_content)
    if svg_mover:
        svg_mover.stop()
    svg_mover = SvgMover(svg_element, interval=50)

async def fetch_svg(file):
    response = await pyfetch(file)
    svg_content = await response.text()
    load_new_svg(svg_content)

upload_form = document.getElementById('upload-form')
upload_form.addEventListener('submit', create_proxy(handle_upload))

async def main():
    file = window.location.search.split('file=')[1] if 'file=' in window.location.search else 'uploads/default.svg'
    await fetch_svg(file)

import asyncio
asyncio.ensure_future(main())
