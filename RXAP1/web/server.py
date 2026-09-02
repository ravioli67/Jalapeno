from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
from datetime import datetime


HOST = "0.0.0.0"
PORT = 44388


# ==========================================
# WEB PAGE
# ==========================================

HTML = """
<!DOCTYPE html>

<html>

<head>

    <meta charset="UTF-8">

    <title>RXAP1</title>

    <style>

        body {
            margin: 0;
            background: #111;
            color: #0f0;
            font-family: monospace;
        }

        header {
            padding: 20px;
            background: #1b1b1b;
            border-bottom: 2px solid #0f0;
        }

        h1 {
            margin: 0;
        }

        #screen {
            margin: 30px;
            padding: 20px;
            min-height: 400px;
            background: #000;
            border: 2px solid #0f0;
            white-space: pre-wrap;
            outline: none;
            overflow-y: auto;
            font-size: 16px;
            line-height: 1.4;
        }

        #cursor {
            animation: blink 1s infinite;
        }

        @keyframes blink {

            50% {
                opacity: 0;
            }

        }

    </style>

</head>


<body>

    <header>

        <h1>RXAP1</h1>

        <div>Z80 Virtual Computer</div>

    </header>


    <div
        id="screen"
        tabindex="0"
    ></div>


<script>

const screen = document.getElementById("screen");


let output = `RXAP1 BOOT OK

CPU: Z80
ROM: OFF
RAM: 64 KB

> `;


let text = "";


function draw() {

    screen.textContent = "";

    screen.appendChild(
        document.createTextNode(
            output + text
        )
    );

    const cursor = document.createElement("span");

    cursor.id = "cursor";

    cursor.textContent = "█";

    screen.appendChild(cursor);

}


draw();

screen.focus();


document.addEventListener(
    "keydown",
    async function(event) {

        event.preventDefault();


        // ==================================
        // NORMAL CHARACTERS
        // ==================================

        if (event.key.length === 1) {

            text += event.key;

            draw();

            return;

        }


        // ==================================
        // BACKSPACE
        // ==================================

        if (event.key === "Backspace") {

            text = text.slice(0, -1);

            draw();

            return;

        }


        // ==================================
        // ENTER
        // ==================================

        if (event.key === "Enter") {

            const command = text;

            output += command + "\\n";

            text = "";

            draw();


            // ==================================
            // SEND TO PYTHON
            // ==================================

            try {

                const response = await fetch(
                    "/input",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/x-www-form-urlencoded"
                        },

                        body:
                            "text=" +
                            encodeURIComponent(command)
                    }
                );


                const data =
                    await response.json();


                // ==================================
                // CLEAR
                // ==================================

                if (
                    command.toLowerCase().trim()
                    === "clear"
                ) {

                    output = "";

                }


                // ==================================
                // NORMAL RESPONSE
                // ==================================

                else if (data.output) {

                    output += data.output;

                }


                output += "> ";

                draw();

            }

            catch (error) {

                output +=
                    "ERROR: Could not reach RXAP1\\n> ";

                draw();

            }

        }

    }
);


</script>


</body>

</html>
"""


# ==========================================
# HTTP HANDLER
# ==========================================

class RXAP1Handler(BaseHTTPRequestHandler):


    # ======================================
    # GET
    # ======================================

    def do_GET(self):

        if self.path == "/":

            content = HTML.encode(
                "utf-8"
            )

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )

            self.send_header(
                "Content-Length",
                str(len(content))
            )

            self.end_headers()

            self.wfile.write(
                content
            )

        else:

            self.send_error(404)


    # ======================================
    # POST
    # ======================================

    def do_POST(self):

        if self.path != "/input":

            self.send_error(404)

            return


        # ==================================
        # READ REQUEST
        # ==================================

        length = int(
            self.headers.get(
                "Content-Length",
                0
            )
        )


        body = self.rfile.read(
            length
        ).decode(
            "utf-8"
        )


        data = parse_qs(
            body
        )


        text = data.get(
            "text",
            [""]
        )[0]


        # ==================================
        # PYTHON TERMINAL
        # ==================================

        print(
            f"RXAP1 INPUT: {text}"
        )


        # ==================================
        # CLEAN COMMAND
        # ==================================

        command = text.strip()

        lower_command = command.lower()


        # ==================================
        # COMMANDS
        # ==================================

        if lower_command == "help":

            response = (
                "RXAP1 COMMANDS\n"
                "---------------\n"
                "help     - show commands\n"
                "clear    - clear screen\n"
                "status   - computer status\n"
                "about    - information about RXAP1\n"
                "version  - show RXAP1 version\n"
                "cpu      - show CPU information\n"
                "memory   - show memory information\n"
                "echo     - print text\n"
                "hello    - say hello\n"
                "time     - show current time\n"
            )


        elif lower_command == "status":

            response = (
                "RXAP1 STATUS\n"
                "------------\n"
                "CPU: Z80\n"
                "ROM: OFF\n"
                "RAM: 64 KB\n"
                "SYSTEM: ONLINE\n"
            )


        elif lower_command == "about":

            response = (
                "RXAP1\n"
                "-----\n"
                "RXAP1 is a virtual 8-bit computer.\n"
                "Architecture: Z80\n"
                "Memory: 64 KB\n"
                "Status: Running\n"
            )


        elif lower_command == "version":

            response = (
                "RXAP1 version 0.1.0\n"
            )


        elif lower_command == "cpu":

            response = (
                "CPU INFORMATION\n"
                "---------------\n"
                "Processor: Z80\n"
                "Architecture: 8-bit\n"
                "Address bus: 16-bit\n"
                "Address space: 64 KB\n"
            )


        elif lower_command == "memory":

            response = (
                "MEMORY INFORMATION\n"
                "------------------\n"
                "RAM: 64 KB\n"
                "ROM: 4 KB\n"
                "Address space: 0000-FFFF\n"
            )


        elif lower_command == "hello":

            response = (
                "Hello from RXAP1!\n"
            )


        elif lower_command == "time":

            response = (
                "RXAP1 TIME\n"
                "----------\n"
                + datetime.now().strftime("%H:%M:%S")
                + "\n"
            )


        elif lower_command.startswith("echo "):

            response = (
                command[5:]
                + "\n"
            )


        elif lower_command == "clear":

            response = ""


        else:

            response = (
                "Unknown command: "
                + command
                + "\n"
                "Type 'help' for a list of commands.\n"
            )


        # ==================================
        # SEND RESPONSE
        # ==================================

        result = json.dumps(
            {
                "output": response
            }
        ).encode(
            "utf-8"
        )


        self.send_response(200)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.send_header(
            "Content-Length",
            str(len(result))
        )

        self.end_headers()

        self.wfile.write(
            result
        )


    # ======================================
    # HIDE HTTP LOGS
    # ======================================

    def log_message(
        self,
        format,
        *args
    ):

        return


# ==========================================
# START SERVER
# ==========================================

def start_server():

    server = HTTPServer(
        (HOST, PORT),
        RXAP1Handler
    )


    print("=" * 50)
    print("          RXAP1 WEB COMPUTER")
    print("=" * 50)
    print()

    print(
        f"Server running on port {PORT}"
    )

    print()

    print(
        "Press CTRL+C to stop."
    )

    print()

    server.serve_forever()


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    start_server()