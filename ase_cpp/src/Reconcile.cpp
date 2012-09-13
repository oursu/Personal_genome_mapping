#include "swak/Swak.h"
#include "swak/System.h"
#include "swak/Helpers.h"
#include "BamReader.h"
#include "BamWriter.h"
#include "BamUtil.h"

using namespace BamTools;
using namespace BamUtil;

namespace Reconcile
{
    // User args
    string bam_file1;
    string bam_file2;
    string out_bam_file;
    
    // User options
    string readgroup_1 = "bam1";
    string readgroup_2 = "bam2";
    
    // Program vars
    vector<string> args;
    YAML::Node options;
    
    BamReader bam_reader1;
    BamReader bam_reader2;
    BamWriter bam_writer;
    
    const string readgroup_ambig = "ambiguous";
    
    void ProcessCmdLine(const vector<string> &all_args)
    {
        int num_args = 3;
        int num_prog_names = 2;
        
        if (!ProcessInput(all_args, num_prog_names, num_args, options, args))
        {
            string usage = Basename(all_args[0]) + " reconcile [options] <in1.bam> <in2.bam> <out.bam>";
            string desc = "Assumes <in1.bam> and <in2.bam> are sorted by read name. Also pair read is assumed.";
            
            VecS opt_lines;
            opt_lines.push_back("rg1=STR name for read group [" + readgroup_1 + "]");
            opt_lines.push_back("rg2=STR name for read group [" + readgroup_2 + "]");
            
            PrintUsage(usage, desc, opt_lines);
            exit(0);
        }
        
        YAML::SetVar(options, "rg1", readgroup_1, false);
        YAML::SetVar(options, "rg2", readgroup_2, false);
        
        bam_file1 = args[0];
        bam_file2 = args[1];
        out_bam_file = args[2];
    }
    
    void Init()
    {
        cerr << "* Initializing" << endl;
        OpenBam(bam_reader1, bam_file1);
        OpenBam(bam_reader2, bam_file2);
        
        SamHeader header = bam_reader1.GetHeader();
        SamHeader header2 = bam_reader2.GetHeader();
        
        SamReadGroup rg1_obj;
        rg1_obj.ID = readgroup_1;
        rg1_obj.Sample = readgroup_1;
        rg1_obj.Library = readgroup_1;
        SamReadGroup rg2_obj;
        rg2_obj.ID = readgroup_2;
        rg2_obj.Sample = readgroup_2;
        rg2_obj.Library = readgroup_2;
        SamReadGroup rgamb_obj;
        rgamb_obj.ID = readgroup_ambig;
        rgamb_obj.Sample = readgroup_ambig;
        rgamb_obj.Library = readgroup_ambig;
        header.ReadGroups.Clear();
        header.ReadGroups.Add(rg1_obj);
        header.ReadGroups.Add(rg2_obj);
        header.ReadGroups.Add(rgamb_obj);
        
        OpenBam(bam_writer, out_bam_file, header, bam_reader1.GetReferenceData());
        
        // TODO: Make deterministic
        srand48(0xCAFEBABA);
    }
    
};


using namespace Reconcile;

int main_reconcile(const vector<string> &all_args)
{
    ProcessCmdLine(all_args);
    Init();
    
    BamAlignment bam1_f;
    BamAlignment bam1_l;
    BamAlignment bam2_f;
    BamAlignment bam2_l;
    
    int64 num_reads = 0;
    int64 num_bam1 = 0;
    int64 num_bam2 = 0;
    int64 num_amb = 0;
    
    bool exit1_f;
    bool exit1_l;
    bool exit2_f;
    bool exit2_l;
    
    BamAlignment * bam_ptr_f = NULL;
    BamAlignment * bam_ptr_l = NULL;
    
    while(1)
    {
        exit1_f = bam_reader1.GetNextAlignment(bam1_f);
        exit1_l = bam_reader1.GetNextAlignment(bam1_l);
        exit2_f = bam_reader2.GetNextAlignment(bam2_f);
        exit2_l = bam_reader2.GetNextAlignment(bam2_l);
        
        if (!(exit1_f && exit1_l && exit2_f && exit2_l))
        {
            break;
        }
        
        
        while (1)
        {
            if (bam1_f.Name >= bam2_f.Name && bam1_l.Name >= bam2_l.Name)
            {
                break;
            }
            
            bam_ptr_f = &bam1_f;
            bam_ptr_l = &bam1_l;
            bam_ptr_f->RemoveTag("XC");
            bam_ptr_f->AddTag("XC", "Z", "one_missing");
            bam_ptr_l->RemoveTag("XC");
            bam_ptr_l->AddTag("XC", "Z", "one_missing");
            bam_ptr_f->EditTag("RG", "Z", readgroup_1);
            bam_ptr_l->EditTag("RG", "Z", readgroup_1);
            
            bam_writer.SaveAlignment(*bam_ptr_f);
            bam_writer.SaveAlignment(*bam_ptr_l);
            
            num_reads ++;
            num_bam1 ++;
            
            if (!(bam_reader1.GetNextAlignment(bam1_f) && bam_reader1.GetNextAlignment(bam1_l)))
            {
                break;
            }
        }
        
        while (1)
        {
            if (bam1_f.Name <= bam2_f.Name && bam1_l.Name <= bam2_l.Name)
            {
                break;
            }
            
            bam_ptr_f = &bam2_f;
            bam_ptr_l = &bam2_l;
            bam_ptr_f->RemoveTag("XC");
            bam_ptr_f->AddTag("XC", "Z", "one_missing");
            bam_ptr_l->RemoveTag("XC");
            bam_ptr_l->AddTag("XC", "Z", "one_missing");
            bam_ptr_f->EditTag("RG", "Z", readgroup_2);
            bam_ptr_l->EditTag("RG", "Z", readgroup_2);
            
            bam_writer.SaveAlignment(*bam_ptr_f);
            bam_writer.SaveAlignment(*bam_ptr_l);
            
            num_reads ++;
            num_bam2 ++;
            
            if (!(bam_reader2.GetNextAlignment(bam2_f) && bam_reader2.GetNextAlignment(bam2_l)))
            {
                break;
            }
        }
        
        num_reads ++;
        
        if (!bam1_f.IsFirstMate())
        {
            swap(bam1_f, bam1_l);
        }
        if (!bam2_f.IsFirstMate())
        {
            swap(bam2_f, bam2_l);
        }
        
        int edit_dist1_f = INT_MAX;
        int edit_dist1_l = INT_MAX;
        int edit_dist2_f = INT_MAX;
        int edit_dist2_l = INT_MAX;
        
        if ((!bam1_f.IsMapped() || !bam1_l.IsMapped()) && (!bam2_f.IsMapped() || !bam2_l.IsMapped()))
        {
            if (lrand48() % 2 == 0)
            {
                bam_ptr_f = &bam1_f;
                bam_ptr_l = &bam1_l;
            }
            else
            {
                bam_ptr_f = &bam2_f;
                bam_ptr_l = &bam2_l;
            }
            bam_ptr_f->RemoveTag("XC");
            bam_ptr_f->AddTag("XC", "Z", "both_unmap");
            bam_ptr_l->RemoveTag("XC");
            bam_ptr_l->AddTag("XC", "Z", "both_unmap");
            bam_ptr_f->EditTag("RG", "Z", "ambiguous");
            bam_ptr_l->EditTag("RG", "Z", "ambiguous");
            num_amb ++;
        }
        else if ((bam1_f.IsMapped() && bam1_l.IsMapped()) && (!bam2_f.IsMapped() || !bam2_l.IsMapped()))
        {
            bam_ptr_f = &bam1_f;
            bam_ptr_l = &bam1_l;
            bam_ptr_f->RemoveTag("XC");
            bam_ptr_f->AddTag("XC", "Z", "one_unmap");
            bam_ptr_l->RemoveTag("XC");
            bam_ptr_l->AddTag("XC", "Z", "one_unmap");
            bam_ptr_f->EditTag("RG", "Z", readgroup_1);
            bam_ptr_l->EditTag("RG", "Z", readgroup_1);
            num_bam1 ++;
        }
        else if ((!bam1_f.IsMapped() || !bam1_l.IsMapped()) && (bam2_f.IsMapped() && bam2_l.IsMapped()))
        {
            bam_ptr_f = &bam2_f;
            bam_ptr_l = &bam2_l;
            
            bam_ptr_f->RemoveTag("XC");
            bam_ptr_f->AddTag("XC", "Z", "one_unmap");
            bam_ptr_l->RemoveTag("XC");
            bam_ptr_l->AddTag("XC", "Z", "one_unmap");
            bam_ptr_f->EditTag("RG", "Z", readgroup_2);
            bam_ptr_l->EditTag("RG", "Z", readgroup_2);
            num_bam2 ++;
        }
        else
        {
            Assert(bam1_f.GetTag("NM", edit_dist1_f));
            Assert(bam1_l.GetTag("NM", edit_dist1_l));
            Assert(bam2_f.GetTag("NM", edit_dist2_f));
            Assert(bam2_l.GetTag("NM", edit_dist2_l));
            if ((edit_dist1_f < edit_dist2_f && edit_dist1_l <= edit_dist2_l) || (edit_dist1_f <= edit_dist2_f && edit_dist1_l < edit_dist2_l))
            {
                bam_ptr_f = &bam1_f;
                bam_ptr_l = &bam1_l;
                bam_ptr_f->EditTag("RG", "Z", readgroup_1);
                bam_ptr_l->EditTag("RG", "Z", readgroup_1);
                num_bam1 ++;
            }
            else if ((edit_dist1_f > edit_dist2_f && edit_dist1_l >= edit_dist2_l) ||(edit_dist1_f >= edit_dist2_f && edit_dist1_l > edit_dist2_l))
            {
                bam_ptr_f = &bam2_f;
                bam_ptr_l = &bam2_l;
                bam_ptr_f->EditTag("RG", "Z", readgroup_2);
                bam_ptr_l->EditTag("RG", "Z", readgroup_2);
                num_bam2 ++;
            }
            else
            {
                if (lrand48() % 2 == 0)
                {
                    bam_ptr_f = &bam1_f;
                    bam_ptr_l = &bam1_l;
                }
                else
                {
                    bam_ptr_f = &bam2_f;
                    bam_ptr_l = &bam2_l;
                }
                bam_ptr_f->EditTag("RG", "Z", "ambiguous");
                bam_ptr_l->EditTag("RG", "Z", "ambiguous");
                num_amb ++;
            }
            if (bam1_f.Position == bam2_f.Position && bam1_l.Position == bam2_l.Position)
            {
                bam_ptr_f->RemoveTag("XC");
                bam_ptr_f->AddTag("XC", "Z", "same_pos");
                bam_ptr_l->RemoveTag("XC");
                bam_ptr_l->AddTag("XC", "Z", "same_pos");
            }
            else
            {
                bam_ptr_f->RemoveTag("XC");
                bam_ptr_f->AddTag("XC", "Z", "diff_pos");
                bam_ptr_l->RemoveTag("XC");
                bam_ptr_l->AddTag("XC", "Z", "diff_pos");
                string RGtag;
                bam_ptr_f->GetTag("RG", RGtag);
                if (RGtag == "ambiguous")
                {
                    bam_ptr_f->MapQuality = 0;
                    bam_ptr_l->MapQuality = 0;
                }
            }
        }
        bam_writer.SaveAlignment(*bam_ptr_f);
        bam_writer.SaveAlignment(*bam_ptr_l);
        
        if (num_reads % 1000 == 0)
        {
            cerr << "* Alignments processed so far: " << num_reads << "\r";
            cerr.flush();
        }
    }
    
    if ((exit1_f && exit1_l) && !(exit2_f && exit2_l))
    {
        while (1)
        {
            bam_ptr_f = &bam1_f;
            bam_ptr_l = &bam1_l;
            bam_ptr_f->RemoveTag("XC");
            bam_ptr_f->AddTag("XC", "Z", "one_missing");
            bam_ptr_l->RemoveTag("XC");
            bam_ptr_l->AddTag("XC", "Z", "one_missing");
            bam_ptr_f->EditTag("RG", "Z", readgroup_1);
            bam_ptr_l->EditTag("RG", "Z", readgroup_1);
            
            bam_writer.SaveAlignment(*bam_ptr_f);
            bam_writer.SaveAlignment(*bam_ptr_l);
            
            num_reads ++;
            num_bam1 ++;
            
            if (!(bam_reader1.GetNextAlignment(bam1_f) && bam_reader1.GetNextAlignment(bam1_l)))
            {
                break;
            }
        }
    }
    
    if (!(exit1_f && exit1_l) && (exit2_f && exit2_l))
    {
        while (1)
        {
            bam_ptr_f = &bam2_f;
            bam_ptr_l = &bam2_l;
            bam_ptr_f->RemoveTag("XC");
            bam_ptr_f->AddTag("XC", "Z", "one_missing");
            bam_ptr_l->RemoveTag("XC");
            bam_ptr_l->AddTag("XC", "Z", "one_missing");
            bam_ptr_f->EditTag("RG", "Z", readgroup_2);
            bam_ptr_l->EditTag("RG", "Z", readgroup_2);
            
            bam_writer.SaveAlignment(*bam_ptr_f);
            bam_writer.SaveAlignment(*bam_ptr_l);
            
            num_reads ++;
            num_bam2 ++;
            
            if (!(bam_reader2.GetNextAlignment(bam2_f) && bam_reader2.GetNextAlignment(bam2_l)))
            {
                break;
            }
        }
    }
    
    cerr << endl;
    Assert(!bam_reader1.GetNextAlignment(bam1_f) && !bam_reader2.GetNextAlignment(bam2_f));
    cout << "* Total alignments processed: \t" << num_reads << endl;
    
    cout << "* Num in readgroup " << ToStrL(readgroup_1 + ":", 11) << "\t" << ToStrL(num_bam1, 10) << "\t" << ToPercent(num_bam1, num_reads) << endl;
    cout << "* Num in readgroup " << ToStrL(readgroup_2 + ":", 11) << "\t" << ToStrL(num_bam2, 10) << "\t" << ToPercent(num_bam2, num_reads) << endl;
    cout << "* Num in readgroup amb:       \t" << ToStrL(num_amb, 10) << "\t" << ToPercent(num_amb, num_reads) << endl;
    
    return 0;
}
