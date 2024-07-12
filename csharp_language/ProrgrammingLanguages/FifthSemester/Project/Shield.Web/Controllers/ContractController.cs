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
        return Ok(new GetAllContractsResponse() { Contracts = _context.Contracts.Include(c => c.Picture).Select(entity => new ContractDto()
        {
            ContractId = entity.ContractId,
            Address = entity.Address,
            Owners = entity.Owners,
            Bailee = entity.Bailee,
            Comment = entity.Comment,
            SignDate = entity.SignDate,
            Picture = new PictureDto()
            {
                PictureId = entity.Picture.PictureId,
                Title = entity.Picture.Title,
                Type = entity.Picture.Type,
                Data = entity.Picture.Data
            }
        }).ToList() });
    }

    [HttpPost]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> CreateContract([FromBody] ContractDto contract)
    {
        var c = new Contract
        {
            Address = contract.Address,
            Comment = contract.Comment,
            Owners = contract.Owners,
            Bailee = contract.Bailee,
            SignDate = contract.SignDate
        };

        var plan = new Plan()
        {
            Title = contract.Plan.Title,
            Type = contract.Plan.Type,
            Data = contract.Plan.Data,
            Contract = c
        };

        var picture = new Picture()
        {
            Title = contract.Picture.Title,
            Type = contract.Picture.Type,
            Data = contract.Picture.Data,
            Contract = c
        };

        c.Plan = plan;
        c.Picture = picture;

        var entity = (await _context.Contracts.AddAsync(c)).Entity;
        //await _context.Plans.AddAsync(plan);
        //await _context.Pictures.AddAsync(picture);

        await _context.SaveChangesAsync();

        return Ok(new ContractDto()
        {
            ContractId = entity.ContractId,
            Address = entity.Address,
            Owners = entity.Owners,
            Bailee = entity.Bailee,
            Comment = entity.Comment,
            SignDate = entity.SignDate,
            Plan = new PlanDto()
            {
                PlanId = entity.Plan.PlanId,
                Title = entity.Plan.Title,
                Type = entity.Plan.Type,
                Data = entity.Plan.Data
            },
            Picture = new PictureDto()
            {
                PictureId = entity.Picture.PictureId,
                Title = entity.Picture.Title,
                Type = entity.Picture.Type,
                Data = entity.Picture.Data
            }
        });
    }

    [HttpGet("{id}")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> GetContract([FromRoute] int id)
    {
        var entity = await _context.Contracts.Include(c => c.Plan).Include(c => c.Picture).FirstOrDefaultAsync(c => c.ContractId == id);
        if (entity != null) return Ok(new ContractDto()
        {
            ContractId = entity.ContractId,
            Address = entity.Address,
            Owners = entity.Owners,
            Bailee = entity.Bailee,
            Comment = entity.Comment,
            SignDate = entity.SignDate,
            Plan = new PlanDto()
            {
                PlanId = entity.Plan.PlanId,
                Title = entity.Plan.Title,
                Type = entity.Plan.Type,
                Data = entity.Plan.Data
            },
            Picture = new PictureDto()
            {
                PictureId = entity.Picture.PictureId,
                Title = entity.Picture.Title,
                Type = entity.Picture.Type,
                Data = entity.Picture.Data
            }
        });
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
        //var contract = await _context.Contracts.FindAsync(id);
        //if (contract != null)
        //{
        //    contract.Address = dto.Address;
        //    contract.Plan = dto.Plan;
        //    contract.Owners = string.Join(";", dto.Owners);
        //    contract.Bailee = dto.Bailee;

        //    await _context.SaveChangesAsync();
        //    return Ok();
        //}
        //else
        return NotFound();
    }
}
