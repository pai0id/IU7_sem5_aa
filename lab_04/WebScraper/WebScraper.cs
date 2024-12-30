using System.Collections.Concurrent;
using System.Text.RegularExpressions;
using System.Threading;
using HtmlAgilityPack;

namespace lab_04.WebScraper {
    public class WebScraper
    {
        private readonly HttpClient _httpClient = new();
        private readonly Uri _baseUri;
        private readonly int _maxPages;
        private readonly string _outputDirectory;
        private readonly ConcurrentQueue<string> _urlQueue = new();
        private readonly HashSet<string> _processedUrls = [];
        // private readonly SemaphoreSlim _semaphore;
        private readonly System.Threading.Mutex _lockQueue = new();
        private readonly System.Threading.Mutex _lockProcessedUrls = new();
        readonly int _maxTreads;
        int cnt;

        public WebScraper(string baseUrl, int maxPages, string outputDirectory, int maxThreads = 1)
        {
            _baseUri = new Uri(baseUrl);
            _maxPages = maxPages;
            _outputDirectory = outputDirectory;
            Directory.CreateDirectory(_outputDirectory);
            _maxTreads = maxThreads;
            cnt = 0;
        }

        public void StartScraping(bool parallelMode = false)
        {
            _urlQueue.Enqueue(_baseUri.ToString());

            if (parallelMode)
            {
                var threads = new List<Thread>();
                for (int i = 0; i < _maxTreads; i++)
                {
                    var thread = new Thread(ProcessQueueParallel);
                    threads.Add(thread);
                    thread.Start();
                }

                foreach (var thread in threads)
                {
                    thread.Join();
                }
            }
            else
            {
                ProcessQueueSequential();
            }
        }

        private void ProcessQueueSequential()
        {
            while (_urlQueue.TryDequeue(out string url) && _processedUrls.Count < _maxPages)
            {
                ProcessPage(url);
            }
        }

        private void ProcessQueueParallel()
        {
            bool flag;
            string url;
            while (cnt < _maxPages)
            {
                flag = false;
                lock (_lockQueue)
                {
                    flag = _urlQueue.TryDequeue(out url);
                }
                if (flag)
                {
                    ProcessPage(url);
                }
                else
                {
                    break;
                }
            }
        }

        private void ProcessPage(string url)
        {
            if (!Uri.TryCreate(url, UriKind.Absolute, out Uri uri) || uri.Host != _baseUri.Host)
                return;

            bool flag = false;
            lock (_lockProcessedUrls)
            {
                if (_processedUrls.Contains(url))
                    flag = true;
                else if (!_processedUrls.Add(url))
                    flag = true;
            }
            if (flag)
                return;

            try
            {
                var response = _httpClient.GetStringAsync(url).Result;
                var filteredContent = ExtractTextFromBody(url, response);

                if (!String.IsNullOrEmpty(filteredContent))
                {
                    var filePath = Path.Combine(_outputDirectory, $"{cnt++}.txt");
                    File.WriteAllText(filePath, filteredContent);
                }

                foreach (var link in ExtractLinks(response))
                {
                    flag = false;
                    lock (_lockProcessedUrls)
                    {
                        flag = _processedUrls.Contains(link);
                    }
                    if (!flag)
                    {
                        lock (_lockQueue)
                        {
                            _urlQueue.Enqueue(link);
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error processing {url}: {ex.Message}");
            }
        }

        static private string ExtractTextFromBody(string url, string htmlContent)
        {
            var doc = new HtmlDocument();
            doc.LoadHtml(htmlContent);

            var sectionExists = doc.DocumentNode.SelectSingleNode("//html/body/section/div/div[3]/div[1]/div[3]/div[1]/ul") != null;

            if (!sectionExists)
            {
                return "";
            }

            var bodyText = new List<string>();

            bodyText.Add(url);

            var xPaths = new[]
            {
                "//html/body/section/div/h1",
                "//html/body/section/div/div[3]/div[1]/div[3]/div[1]/ul",
                "//html/body/section/div/div[3]/div[1]/div[3]/div[2]/ol",
                "//html/body/section/div/div[3]/div[2]/figure/img"
            };

            foreach (var xPath in xPaths)
            {
                var node = doc.DocumentNode.SelectSingleNode(xPath);
                if (node != null)
                {
                    if (xPath == "//html/body/section/div/div[3]/div[1]/div[3]/div[1]/ul")
                    {
                        var listItems = node.SelectNodes("./li");
                        if (listItems != null)
                        {
                            bodyText.Add(string.Join("; ", listItems.Select(li => li.InnerText.Trim())));
                        }
                    }
                    else if (node.Name == "img" && node.Attributes["data-src"] != null)
                    {
                        bodyText.Add($"Image: {node.Attributes["data-src"].Value}");
                    }
                    else
                    {
                        bodyText.Add(Regex.Replace(node.InnerText.Trim(), @"\s{2,}", "\n"));
                    }
                }
            }

            return string.Join("\n\n", bodyText);
        }


        private IEnumerable<string> ExtractLinks(string pageContent)
        {
            var matches = Regex.Matches(pageContent, @"<a\s+(?:[^>]*?\s+)?href=[""'](.*?)[""']", RegexOptions.IgnoreCase);
            foreach (Match match in matches)
            {
                if (Uri.TryCreate(_baseUri, match.Groups[1].Value, out Uri? result))
                {
                    if (result.Host == _baseUri.Host)
                        yield return result.ToString();
                }
            }
        }
    }
}
