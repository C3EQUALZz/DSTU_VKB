using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Shield.Web.Data.Models;
using Shield.Web.Interfaces;
using Microsoft.EntityFrameworkCore;

using Shield.DataAccess.DTOs;

namespace Shield.Web.Controllers;

[ApiController]
[Route("api/user")]
public class AppUserController : ControllerBase
{
    private readonly UserManager<User> _userManager;
    private readonly RoleManager<IdentityRole> _roleManager;
    private readonly SignInManager<User> _signInManager;
    private readonly ITokenService _tokenService;

    public AppUserController(UserManager<User> userManager, ITokenService tokenService, RoleManager<IdentityRole> roleManager, SignInManager<User> signInManager)
    {
        _userManager = userManager;
        _tokenService = tokenService;
        _signInManager = signInManager;
        _roleManager = roleManager;
    }

    [HttpGet]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> GetAll()
    {
        return Ok(await _userManager.Users.ToListAsync());
    }

    [HttpDelete]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> DeleteAll()
    {
        foreach (var user in await _userManager.Users.ToListAsync())
        {
            await _userManager.DeleteAsync(user);
        }

        return NoContent();
    }

    [HttpGet]
    [Route("{username}")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> GetByName([FromRoute] string username)
    {
        var user = await _userManager.FindByNameAsync(username);

        if (user == null)
        {
            return NotFound();
        }

        return Ok(user);
    }

    [HttpDelete]
    [Route("{username}")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> DeleteByName([FromRoute] string username)
    {
        var user = await _userManager.Users.FirstOrDefaultAsync(x => x.UserName == username);

        if (user == null)
        {
            return NotFound();
        }

        await _userManager.DeleteAsync(user);

        return NoContent();
    }

    [HttpPost("login")]
    public async Task<IActionResult> Login(LoginDto dto)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        var user = await _userManager.Users.FirstOrDefaultAsync(x => x.UserName == dto.UserName);

        if (user == null)
        {
            return Unauthorized("Invalid username");
        }

        var result = _signInManager.CheckPasswordSignInAsync(user, dto.Password, false);

        if (!result.IsCompletedSuccessfully) return Unauthorized("Username not found and/or password incorrect");
        
        return Ok(new LoginResponseDto()
        {
            UserName = user.UserName,
            Email = user.Email,
            Token = await _tokenService.CreateToken(user)
        });
    }

    [HttpPost("register")]
    public async Task<IActionResult> Register([FromBody] RegisterDto dto)
    {
        try
        {
            if (!ModelState.IsValid) return BadRequest(ModelState);

            var user = new User
            {
                UserName = dto.UserName,
                Email = dto.Email,
            };

            var createdUser = await _userManager.CreateAsync(user, dto.Password);

            if (createdUser.Succeeded)
            {
                var roleResult = await _userManager.AddToRoleAsync(user, "User");
                if (roleResult.Succeeded)
                {
                    return Ok(new LoginResponseDto
                    {
                        UserName = user.UserName,
                        Email = user.Email,
                        Token = await _tokenService.CreateToken(user)
                    });
                }
                else
                {
                    return StatusCode(500, roleResult.Errors);
                }
            }
            else
            {
                return StatusCode(500, createdUser.Errors);
            }
        }
        catch (Exception ex)
        {
            return StatusCode(500, ex.Message);
        }
    }
}
