from tqdm import tqdm
import argparse
from .raw_page_generator import RawPageGenerator
from .page_generator import PageGenerator
from .page_writer import PageWriter


def write_until(page_generator, page_writer, n_pages):
    for i, page in tqdm(enumerate(page_generator)):
        page_writer.run(page)
        if i == n_pages - 1:
            break


def write_all(page_generator, page_writer):
    for i, page in tqdm(page_generator):
        page_writer.run(page)


def main():
    parser = argparse.ArgumentParser("extract text information from wikipedia xml corpus")
    parser.add_argument('input', help="input file path")
    parser.add_argument('output',  help="output file path")
    parser.add_argument("--format", default="text", choices=["text", "json"], help="output file format")
    parser.add_argument("--workers", type=int, default=None, help="restrict n_workers of parallel processing")
    parser.add_argument("--n-pages", type=int, default=None, help="restrict number of page to write (for debug)")

    args = parser.parse_args()

    raw_page_generator = RawPageGenerator(args.input)
    page_generator = PageGenerator(raw_page_generator, n_workers=args.workers)
    page_writer = PageWriter(args.output, output_format=args.format)

    if args.n_pages is None:
        write_all(page_generator, page_writer)
    else:
        write_until(iter(page_generator), page_writer, args.n_pages)


if __name__ == "__main__":
    main()
