using System.Diagnostics;
using lab_04.WebScraper;

class Program
{
    static void Main(string[] args)
    {
        string startUrl = "https://vkusnoprigotovim.ru";
        string outputDir = "pages";
        int maxPages = 1000;
        string csvPath = "scraping_results.csv";

        int[] threadCounts = [16];
        int numTests = 1;

        using (StreamWriter writer = new(csvPath))
        {
            writer.WriteLine("Mode,ThreadCount,AverageElapsedTime(ms)");

            try
            {
                // long totalTime = 0;

                // for (int i = 0; i < numTests; i++)
                // {
                //     var scraper = new WebScraper(startUrl, maxPages, outputDir);
                //     var stopwatch = Stopwatch.StartNew();
                //     scraper.StartScraping(parallelMode: false);
                //     stopwatch.Stop();

                //     totalTime += stopwatch.ElapsedMilliseconds;
                // }

                // writer.WriteLine($"Unparallel,0,{totalTime / numTests}");
                // Console.WriteLine($"Testing with 0 threads: {totalTime / numTests} ms");

                foreach (var threadCount in threadCounts)
                {
                    long totalTime = 0;

                    for (int i = 0; i < numTests; i++)
                    {
                        var scraper = new WebScraper(startUrl, maxPages, outputDir, threadCount);
                        var stopwatch = Stopwatch.StartNew();
                        scraper.StartScraping(parallelMode: true);
                        stopwatch.Stop();

                        totalTime += stopwatch.ElapsedMilliseconds;
                    }

                    writer.WriteLine($"Parallel,{threadCount},{totalTime / numTests}");
                    Console.WriteLine($"Testing with {threadCount} threads: {totalTime / numTests} ms");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in main: {ex.Message}");
            }
        }

        Console.WriteLine("Testing completed. Results saved to scraping_results.csv");
    }
}
