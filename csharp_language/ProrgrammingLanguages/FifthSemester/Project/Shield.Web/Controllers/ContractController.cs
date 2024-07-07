using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

using Shield.Web.Data.Contexts;
using Shield.DataAccess.DTOs;
using Shield.DataAccess.Models;

using Microsoft.EntityFrameworkCore;

namespace Shield.Web.Controllers;

[Route("api/contract")]
[ApiController]
public class ContractController : ControllerBase
{
    private readonly DataContext _context;

    public ContractController(DataContext context) 
    { 
        _context = context;
    }

    [HttpGet]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> GetAllContracts()
    {
        return Ok(new GetAllContractsResponse() { Contracts=_context.Contracts.Include(c => c.Picture).ToList() });
    }

    [HttpPost]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> CreateContract([FromBody] Contract contract)
    {
        var pictureEntity = await _context.Pictures.AddAsync(contract.Picture);
        var planEntity = await _context.Plans.AddAsync(contract.Plan);
        var contractEntity = await _context.Contracts.AddAsync(new Contract { Address=contract.Address, Plan=planEntity.Entity, Owners=contract.Owners, Bailee=contract.Bailee, Comment=contract.Comment, Picture=pictureEntity.Entity });
        await _context.SaveChangesAsync();
        return Ok(contractEntity.Entity);
    }

    [HttpGet("{id}")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> GetContract([FromRoute] int id)
    {
        var contract = await _context.Contracts.Include(c => c.Plan).Include(c => c.Picture).FirstOrDefaultAsync(c => c.ContractId == id);
        if (contract != null) return Ok(contract);
        else return NotFound();
    }

    [HttpDelete("{id}")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> DeleteContract([FromRoute] int id)
    {
        var contract = await _context.Contracts.FindAsync(id);
        if (contract != null)
        {
            _context.Contracts.Remove(contract);
            await _context.SaveChangesAsync();
            return Ok(contract);
        }
        else return NotFound();
    }

    [HttpPut("{id}")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> UpdateContract([FromRoute] int id, [FromBody] ContractDto dto)
    {
        var contract = await _context.Contracts.FindAsync(id);
        if (contract != null)
        {
            contract.Address = dto.Address;
            contract.Plan = dto.Plan;
            contract.Owners = string.Join(";", dto.Owners);
            contract.Bailee = dto.Bailee;

            await _context.SaveChangesAsync();
            return Ok();
        }
        else return NotFound();
    }
}
