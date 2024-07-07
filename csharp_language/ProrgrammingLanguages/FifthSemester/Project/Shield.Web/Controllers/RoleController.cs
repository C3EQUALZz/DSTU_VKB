using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Shield.Web.Data.Models;
using Microsoft.EntityFrameworkCore;

using Shield.DataAccess.DTOs;

namespace Shield.Web.Controllers;

[Route("api/roles")]
[ApiController]
public class RoleController : ControllerBase
{
    private readonly UserManager<User> _userManager;
    private readonly RoleManager<IdentityRole> _roleManager;

    public RoleController(UserManager<User> userManager, RoleManager<IdentityRole> roleManager)
    {
        _userManager = userManager;
        _roleManager = roleManager;
    }

    [HttpGet]
    [Authorize(Roles = "Admin")]
    [Route("{username}")]
    public async Task<IActionResult> GetRoles([FromRoute] string username)
    {
        var user = await _userManager.Users.FirstOrDefaultAsync(x => x.UserName == username);

        //var user = await _userManager.Users.FirstOrDefaultAsync(x => x.UserName == HttpContext.User.Identity.Name);

        //return Ok(user.UserName);

        if (user == null)
        {
            return NotFound();
        }

        return Ok(_userManager.GetRolesAsync(user).Result);
    }

    [HttpPost]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> SetRoles([FromBody] RolesInfoDto dto)
    {
        var user = await _userManager.Users.FirstOrDefaultAsync(x => x.UserName == dto.Username);

        if (user == null)
        {
            return NotFound($"User \"{dto.Username}\" not found");
        }

        List<IdentityRole> rolesToAdd = new();

        // Проверим, что запрошенные роли вообще существуют
        foreach (var rolename in dto.Roles)
        {
            var role = await _roleManager.FindByNameAsync(rolename);
            if (role != null) rolesToAdd.Add(role);
        }

        if (rolesToAdd.Count == 0)
        {
            return NotFound($"No available roles found");
        }

        foreach (var role in rolesToAdd)
        {
            var result = await _userManager.AddToRoleAsync(user, role.Name);

            if (!result.Succeeded)
            {
                return StatusCode(500, result.Errors);
            }
        }

        return Ok(new RolesInfoDto() { Username = dto.Username, Roles = _roleManager.Roles.Select(r => r.Name).ToList() });
    }

    [HttpDelete]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> DeleteRoles([FromBody] RolesInfoDto dto)
    {
        var user = await _userManager.Users.FirstOrDefaultAsync(x => x.UserName == dto.Username);

        if (user == null)
        {
            return NotFound($"User \"{dto.Username}\" not found");
        }

        List<IdentityRole> rolesToDelete = new();

        foreach (var rolename in dto.Roles)
        {
            var role = await _roleManager.FindByNameAsync(rolename);
            if (role != null) rolesToDelete.Add(role);
        }

        if (rolesToDelete.Count == 0)
        {
            return NotFound($"No available roles found");
        }

        foreach (var role in rolesToDelete)
        {
            var result = await _userManager.RemoveFromRoleAsync(user, role.Name);

            if (!result.Succeeded)
            {
                return StatusCode(500, result.Errors);
            }
        }

        return Ok(new RolesInfoDto() { Username = dto.Username, Roles = _roleManager.Roles.Select(r => r.Name).ToList() });
    }

    [HttpPost]
    [Authorize(Roles = "Admin")]
    [Route("{role}")]
    public async Task<IActionResult> CreateRole([FromRoute] string role)
    {
        await _roleManager.CreateAsync(new IdentityRole { Name = role });
        return Ok(_roleManager.Roles);
    }

    [HttpDelete]
    [Authorize(Roles = "Admin")]
    [Route("{role}")]
    public async Task<IActionResult> DeleteRole([FromRoute] string role)
    {
        var _role = await _roleManager.FindByNameAsync(role);
        if (_role != null)
        {
            await _roleManager.DeleteAsync(_role);
            return Ok(_roleManager.Roles);
        }
        else
        {
            return BadRequest();
        }
    }
}