using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

public class Author
{
    public string Name { get; set; }
    public Dictionary<string, int> WordFrequency { get; set; }

    public Author(string name)
    {
        Name = name;
        WordFrequency = new Dictionary<string, int>();
    }

    public void AnalyzeText(string text)
    {
        var words = text.Split(new char[] { ' ', '\t', '\n', '\r', '.', ',', '!', '?', ';', ':' }, StringSplitOptions.RemoveEmptyEntries);
        foreach (var word in words)
        {
            var lowerWord = word.ToLower();
            if (WordFrequency.ContainsKey(lowerWord))
            {
                WordFrequency[lowerWord]++;
            }
            else
            {
                WordFrequency[lowerWord] = 1;
            }
        }
    }
}

public class AuthorshipAnalyzer
{
    private List<Author> authors;

    public AuthorshipAnalyzer()
    {
        authors = new List<Author>();
    }

    public void AddAuthor(Author author)
    {
        authors.Add(author);
    }

    public string DetermineAuthor(string text)
    {
        var textAuthor = new Author("Unknown");
        textAuthor.AnalyzeText(text);

        double minDistance = double.MaxValue;
        string bestMatch = "Unknown";

        foreach (var author in authors)
        {
            double distance = CalculateDistance(textAuthor.WordFrequency, author.WordFrequency);
            if (distance < minDistance)
            {
                minDistance = distance;
                bestMatch = author.Name;
            }
        }

        return bestMatch;
    }

    private double CalculateDistance(Dictionary<string, int> freq1, Dictionary<string, int> freq2)
    {
        var allWords = freq1.Keys.Union(freq2.Keys).ToList();
        double distance = 0;

        foreach (var word in allWords)
        {
            int count1 = freq1.ContainsKey(word) ? freq1[word] : 0;
            int count2 = freq2.ContainsKey(word) ? freq2[word] : 0;
            distance += Math.Pow(count1 - count2, 2);
        }

        return Math.Sqrt(distance);
    }
}

class Program
{
    static void Main(string[] args)
    {
        var analyzer = new AuthorshipAnalyzer();

        // Добавляем известных авторов и их тексты
        var author1 = new Author("Author1");
        author1.AnalyzeText(File.ReadAllText("author1_text.txt"));
        analyzer.AddAuthor(author1);

        var author2 = new Author("Author2");
        author2.AnalyzeText(File.ReadAllText("author2_text.txt"));
        analyzer.AddAuthor(author2);

        // Определяем автора неизвестного текста
        string unknownText = File.ReadAllText("unknown_text.txt");
        string determinedAuthor = analyzer.DetermineAuthor(unknownText);

        Console.WriteLine($"The most likely author of the unknown text is: {determinedAuthor}");
    }
}