using System.Net.Http.Json;
using Windows.Storage;

using Shield.DataAccess.DTOs;

namespace Shield.App.Helpers;
public class ApiHelper
{
    private static string _baseAddress = "http://127.0.0.1:5277/api";
    private static HttpClient _sharedClient = new();
    private static string? _token => (string?)ApplicationData.Current.LocalSettings.Values["apiToken"];

    public static async Task<HttpResponseMessage?> CheckConnection()
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/user/check");
        request.Method = HttpMethod.Get;
        request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _token);

        return await _sharedClient.SendAsync(request);
    }
    
    public static async Task<HttpResponseMessage?> Login(string name, string password)
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/user/login");
        request.Method = HttpMethod.Post;
        request.Content = JsonContent.Create(new LoginDto() { UserName=name, Password=password });

        var response = await _sharedClient.SendAsync(request);

        return response;
    }
    public static async Task<HttpResponseMessage?> Register(string name, string password, string email)
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/user/register");
        request.Method = HttpMethod.Post;
        request.Content = JsonContent.Create(new RegisterDto() { UserName = name, Password = password, Email = email });

        return await _sharedClient.SendAsync(request);
    }
    
    public static async Task<HttpResponseMessage?> Me()
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/user/me");
        request.Method = HttpMethod.Get;
        request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _token);

        return await _sharedClient.SendAsync(request);
    }
    public static async Task<HttpResponseMessage?> GetUserProfile(string id)
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/user/profile/{id}");
        request.Method = HttpMethod.Get;
        request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _token);

        return await _sharedClient.SendAsync(request);
    }
    public static async Task<HttpResponseMessage?> GetAllContracts()
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/contract");
        request.Method = HttpMethod.Get;
        request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _token);

        return await _sharedClient.SendAsync(request);
    }
    public static async Task<HttpResponseMessage?> CreateContract(ContractDto contract)
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/contract");
        request.Method = HttpMethod.Post;
        request.Content = JsonContent.Create(contract);
        request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _token);

        var response = await _sharedClient.SendAsync(request);

        return response;
    }
    public static async Task<HttpResponseMessage?> GetContractFull(int id)
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/contract/{id}");
        request.Method = HttpMethod.Get;
        request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _token);

        var response = await _sharedClient.SendAsync(request);

        return response;
    }
    public static async Task<HttpResponseMessage?> GetContractInfo(int id)
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/contract/{id}F");
        request.Method = HttpMethod.Get;
        request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _token);

        var response = await _sharedClient.SendAsync(request);

        return response;
    }
    public static async Task<HttpResponseMessage?> DeleteContract(int id)
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/contract/{id}");
        request.Method = HttpMethod.Delete;
        request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _token);

        var response = await _sharedClient.SendAsync(request);

        return response;
    }
    public static async Task<HttpResponseMessage?> UpdateContract(int id, ContractDto replacer)
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/contract/{id}");
        request.Method = HttpMethod.Put;

        var dto = new UpdateContractDto()
        {
            Address = replacer.Address,
            Bailee = replacer.Bailee,
            Owners = replacer.Owners,
            Comment = replacer.Comment,
            Organization = replacer.Organization,
        };

        if (replacer.Plan != null)
        {
            dto.Plan = replacer.Plan;
        }

        if (replacer.Picture != null)
        {
            dto.Picture = replacer.Picture;
        }

        request.Content = JsonContent.Create(dto);
        request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _token);
        
        var response = await _sharedClient.SendAsync(request);

        return response;
    }
    public static async Task<HttpResponseMessage?> GetAllAlarms()
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/alarm");
        request.Method = HttpMethod.Get;
        request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _token);

        var response = await _sharedClient.SendAsync(request);

        return response;
    }
    public static async Task<HttpResponseMessage?> CreateAlarm(CreateAlarmDto alarm)
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/alarm");
        request.Method = HttpMethod.Post;
        request.Content = JsonContent.Create(alarm);
        request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _token);

        var response = await _sharedClient.SendAsync(request);

        return response;
    }
    
    private class LoginDto
    {
        public string UserName { get; set; }
        public string Password { get; set; }
    }
    private class RegisterDto
    {
        public string UserName { get; set; }
        public string Email { get; set; }
        public string Password { get; set; }
    }
}