namespace Shield.DataAccess.DTOs;
public class HttpResponseDto
{
    public string Type { get; set; }
    public string Title { get; set; }
    public int Status { get; set; }
    public IDictionary<string, List<string>> Errors { get; set; }
    public string TraceId { get; set; }
}
