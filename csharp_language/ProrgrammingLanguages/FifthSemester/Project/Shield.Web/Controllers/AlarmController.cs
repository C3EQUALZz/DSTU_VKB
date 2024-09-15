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
        return Ok(_context.Alarms.Include(a => a.Contract).Select(a => new AlarmDto()
        {
            AlarmId = a.AlarmId,
            Date = a.Date,
            Result = a.Result,
            Contract = new ContractDto()
            {
                ContractId = a.Contract.ContractId,
                Address = a.Contract.Address,
                Owners = a.Contract.Owners,
                Bailee = a.Contract.Bailee,
                Comment = a.Contract.Comment,
                SignDate = a.Contract.SignDate,
                Organization = a.Contract.Organization,
                IsLegalEntity = a.Contract.IsLegalEntity,
            }
        }).ToList());
    }

    [HttpPost]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> CreateAlarm(CreateAlarmDto dto)
    {
        var contract = await _context.Contracts.FirstOrDefaultAsync(c => c.ContractId == dto.ContractId);

        if (contract == null)
        {
            return NotFound();
        }

        var alarm = new Alarm()
        {
            Date = dto.Date,
            Contract = contract,
            Result = dto.Result,
        };

        var entry = await _context.Alarms.AddAsync(alarm);
        var entity = entry.Entity;

        await _context.SaveChangesAsync();

        return Ok();
    }
}
