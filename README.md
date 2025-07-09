# Static Site Generator

This is a simple, file-based static site generator written in Python. It converts a directory of Markdown files into a complete HTML website, applying a consistent template and styling.

## How It Works

The generator performs the following steps:
1.  **Clears the Output Directory**: It starts by deleting the `docs/` directory to ensure a clean build.
2.  **Copies Static Assets**: It recursively copies all files and directories from the `static/` directory to the `docs/` directory.
3.  **Generates HTML Pages**: It recursively traverses the `content/` directory, and for each Markdown file it finds, it:
    *   Reads the Markdown content.
    *   Extracts the main heading (`# `) to use as the page title.
    *   Converts the Markdown to HTML.
    *   Injects the title and HTML content into the `template.html` file.
    *   Saves the final HTML file to the `docs/` directory, preserving the original directory structure.

## How to Use

1.  **Add Content**: Create or edit Markdown files in the `content/` directory. The directory structure you create here will be mirrored in the final website.
2.  **Add Static Files**: Place your CSS, images, and other static assets in the `static/` directory.
3.  **Build the Site**: Run the `build.sh` script to generate the website:
    ```bash
    ./build.sh
    ```
4.  **View the Site**: Open the `docs/index.html` file in your browser to see the generated website.

You can also use the `main.sh` script to build the site and start a local server:
```bash
./main.sh
```
This will make the site available at `http://localhost:8888`.

## Project Structure

-   `content/`: Contains the Markdown source files for your website.
-   `static/`: Contains static assets like CSS and images.
-   `src/`: Contains the Python source code for the generator.
-   `docs/`: The output directory where the generated HTML files are saved.
-   `template.html`: The master HTML template for all pages.
-   `build.sh`: The script to build the website.
-   `main.sh`: The script to build the website and run a local server.
