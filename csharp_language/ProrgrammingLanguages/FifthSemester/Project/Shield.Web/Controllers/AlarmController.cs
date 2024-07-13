using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;

using Shield.Web.Data.Contexts;
using Shield.DataAccess.DTOs;
using Shield.DataAccess.Models;


namespace Shield.Web.Controllers;

[Route("api/alarm")]
[ApiController]
public class AlarmController : ControllerBase
{
    private readonly DataContext _context;

    public AlarmController(DataContext context)
    {
        _context = context;
    }

    [HttpGet]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> GetAllAlarms()
    {
        return Ok(_context.Alarms.Include(a => a.Contract).ToList());
    }

    [HttpPost]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> CreateAlarm(CreateAlarmDto dto)
    {
        var alarm = new Alarm()
        {
            Date = dto.Date,
            ContractId = dto.ContractId
        };

        var entry = await _context.Alarms.AddAsync(alarm);
        var entity = entry.Entity;

        await _context.SaveChangesAsync();

        return Ok(entity);
    }
}
