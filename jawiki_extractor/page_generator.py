from multiprocessing import cpu_count, Queue, Pool
from .page_parser import PageParser

FINISH_SIGNAL = None


class PageGenerator:
    def __init__(self, raw_page_generator, n_workers=None):
        if n_workers == 1:
            self.generator = SinglePageGenerator(raw_page_generator)
        else:
            self.generator = ParallelPageGenerator(raw_page_generator, n_workers)

    def __iter__(self):
        return iter(self.generator)


class SinglePageGenerator:
    def __init__(self, raw_page_generator):
        self.raw_page_generator = raw_page_generator

    def __iter__(self):
        for raw_page in self.raw_page_generator:
            page = PageParser.parse(raw_page)
            if page.is_acceptable:
                yield page


class ParallelPageGenerator:
    def __init__(self, raw_page_generator, n_workers):
        self.raw_page_generator = raw_page_generator
        self.n_workers = self._decide_n_workers(n_workers)

    def __iter__(self):
        # referenced: https://stackoverflow.com/questions/43078980/python-multiprocessing-with-generator
        raw_page_queue = Queue(maxsize=self.n_workers*10)
        page_queue = Queue(maxsize=self.n_workers*10)
        n_finished_workers = 0

        Pool(
            processes=1,
            initializer=self._fill_raw_page_queue,
            initargs=(raw_page_queue, self.raw_page_generator, self.n_workers)
        )
        Pool(
            processes=self.n_workers,
            initializer=self._worker_process,
            initargs=(raw_page_queue, page_queue)
        )

        while True:
            page = page_queue.get()
            if page is FINISH_SIGNAL:
                n_finished_workers += 1
                if n_finished_workers == self.n_workers:
                    break
            else:
                yield page

    @staticmethod
    def _decide_n_workers(n_workers):
        maximal_workers = cpu_count() - 1

        if n_workers is None:
            return maximal_workers
        else:
            max(maximal_workers, n_workers)

    @staticmethod
    def _fill_raw_page_queue(raw_page_queue, raw_page_generator, n_workers):
        for raw_page in raw_page_generator:
            raw_page_queue.put(raw_page)
        for _ in range(n_workers):
            raw_page_queue.put(FINISH_SIGNAL)

    @staticmethod
    def _worker_process(raw_page_queue, page_queue):
        while True:
            raw_page = raw_page_queue.get()

            if raw_page is FINISH_SIGNAL:
                page_queue.put(FINISH_SIGNAL)
                break

            page = PageParser.parse(raw_page)
            if page.is_acceptable:
                page_queue.put(page)
