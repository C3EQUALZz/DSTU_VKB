using System.Net.Http.Json;
using Windows.Storage;

using Shield.DataAccess.DTOs;
using Shield.DataAccess.Models;

namespace Shield.App.Helpers;
public class ApiHelper
{
    private static string _baseAddress = "http://127.0.0.1:5277/api";
    private static HttpClient _sharedClient = new();
    private static string? _token => (string?)ApplicationData.Current.LocalSettings.Values["apiToken"];

    public static async Task<object?> Login(string name, string password)
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/user/login");
        request.Method = HttpMethod.Post;
        request.Content = JsonContent.Create(new LoginDto() { UserName=name, Password=password });
        ///request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _token);

        try
        {
            var response = await _sharedClient.SendAsync(request);
            var dto = await response.Content.ReadFromJsonAsync<LoginResponseDto>();

            if (dto != null)
            {
                ApplicationData.Current.LocalSettings.Values["apiToken"] = dto.Token;
            }

            return dto;
        }
        catch (Exception ex)
        {
            return ex;
        }
    }

    public static async Task<string?> Register(string name, string password, string email)
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/user/register");
        request.Method = HttpMethod.Post;
        request.Content = JsonContent.Create(new RegisterDto() { UserName = name, Password = password, Email = email });

        try
        {
            var response = await _sharedClient.SendAsync(request);
            return await response.Content.ReadAsStringAsync();
        }
        catch (Exception ex)
        {
            return ex.Message + (ex.InnerException != null ? "\n" + ex.InnerException.Message : "");
        }
    }

    public static async Task<GetAllContractsResponse?> GetAllContracts()
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/contract");
        request.Method = HttpMethod.Get;
        request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _token);

        var response = await _sharedClient.SendAsync(request);
        var dto = await response.Content.ReadFromJsonAsync<GetAllContractsResponse>();

        return dto;
    }

    public static async Task<HttpResponseMessage?> CreateContract(Contract contract)
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/contract");
        request.Method = HttpMethod.Post;
        request.Content = JsonContent.Create(contract);
        request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _token);

        var response = await _sharedClient.SendAsync(request);

        return response;
    }

    public static async Task<HttpResponseMessage?> GetContract(int id)
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/contract/{id}");
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

    public static async Task<HttpResponseMessage?> UpdateContract(int id, Contract replacer)
    {
        using var request = new HttpRequestMessage();
        request.RequestUri = new Uri($"{_baseAddress}/contract/{id}");
        request.Method = HttpMethod.Post;
        request.Content = JsonContent.Create(new ContractDto() { Address = replacer.Address, Plan = replacer.Plan, Owners = replacer.Owners.Split(';').ToList(), Bailee = replacer.Bailee });
        request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _token);
        return null;
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