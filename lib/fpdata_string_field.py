from ..models import Article, ArticleEvidenceRel, Attachment, Evidence, EvidenceFragmentRel, Fragment, ingest_errors
from ..models import article_not_found
from ..models import FiringPattern,FiringPatternRel

# ingests attachment_fp.csv, fp_fragment.csv, fp_definitions.csv, fp_parameters and populates ArticleEvidenceRel, article_not_found, Evidence, EvidenceFragmentRel, FiringPattern, FiringPatternRel, Fragment,
class FiringPatternStringField:
# firing pattern attachment
    def attachment_fp_to_attachment_fp(self):
        row_num=2
        for row in self.rows:
            cell_identifier                 = None
            quote_reference_id              = None
            name_of_file_containing_figure  = None
            figure_table                    = None
            parameter                       = None
            protocol_tag                    = None
            interpretation_notes            = None
            try:
                # set cell_identifier
                if(row['Cell Identifier'].strip()):
                    cell_identifier = int(row['Cell Identifier'].strip())
                # set quote_reference_id
                try:
                    if(row['Quote reference id'].strip()):
                        quote_reference_id = row['Quote reference id']
                        quote_reference_id=int(quote_reference_id)
                except ValueError:
                    quote_reference_id = None
                # set name_of_file_containing_figure
                name_of_file_containing_figure = row['Name of file containing figure']
                if len(name_of_file_containing_figure) == 0:
                    name_of_file_containing_figure = None
                # set figure_table
                try:
                    if(row['Figure/Table'].strip()):
                        figure_table = row['Figure/Table'].strip()
                    else:
                        figure_table = None
                except ValueError:
                    figure_table = None
                # set parameter
                parameter = None
                try:
                    parameter = row['Parameter'].strip()
                    if len(parameter) == 0:
                        parameter = None
                except Exception:
                    parameter = None
                # set interpretation_notes
                try:
                    interpretation_notes = row['Interpretation notes figures'].strip()
                    if len(interpretation_notes) == 0:
                        interpretation_notes = None
                except Exception:
                    interpretation_notes = None
                # write Attachment record
                if(cell_identifier!=None):
                    row_object = Attachment(
                        cell_id              = cell_identifier,
                        original_id          = quote_reference_id,
                        name                 = name_of_file_containing_figure,
                        type                 = figure_table,
                        parameter            = parameter,
                        protocol_tag         = protocol_tag,
                        interpretation_notes = interpretation_notes
                    )
                    row_object.save()                
            except Exception as e:
                if(cell_identifier!=None):
                    try:
                        row_object = ingest_errors.objects.get(file_row_num=row_num,filename='fp_attachment.csv')
                    except ingest_errors.DoesNotExist:
                        row_object = ingest_errors(filename='fp_attachment.csv',file_row_num=row_num,comment=str(e))
                        row_object.save()
                cell_identifier= None
            row_num=row_num+1

    # firing pattern fragment
    def fp_fragment_to_fp_fragment(self):
        row_num=2          # starting header offset
        row_object  = EvidenceFragmentRel.objects.last()
        fragment_id = row_object.Fragment_id + 1                  # initialize from last fragment entry
        for row in self.rows: # is this a morph_fragment.csv file or a marker_fragment.csv file
            reference_id                   = None
            cell_id                        = None
            material_used                  = None
            location_in_reference          = None
            pmid_isbn                      = None
            pmid_isbn_page                 = None
            type                           = None
            article_id                     = None
            attachment                     = None
            attachment_type                = None
            # set reference_id

            try:
                if(row['ReferenceID'].strip()):
                    reference_id = row['ReferenceID'].strip()
                    reference_id = int(reference_id)
                try:
                    material_used = row['Material Used']
                    if len(material_used) == 0:
                        material_used = None
                except Exception:
                    material_used = None
                # cell id    
                try:
                    if(row['Cell ID'].strip()):
                        cell_id = int(row['Cell ID'].strip())
                except Exception:
                    cell_id = None
                # set location_in_reference
                try:
                    location_in_reference = row['Location in reference']
                    if len(location_in_reference) == 0:
                        location_in_reference = None
                except Exception:
                    location_in_reference = None
                # set pmid_isbn
                try:
                    if(row['PMID/ISBN'].replace('-','').strip()):
                        pmid_isbn = int(row['PMID/ISBN'].replace('-',''))
                except Exception:
                    pmid_isbn = None
                # set pmid_isbn_page
                try:
                    pmid_isbn_page = int(row['pmid_isbn_page'])
                except Exception:
                    pmid_isbn_page = None
                # set article_id
                if pmid_isbn == None:
                    article_id = None
                else:
                    row_object = None
                    if pmid_isbn_page != None:
                        if pmid_isbn_page == 0:
                            try:
                                row_object = Article.objects.filter(pmid_isbn=pmid_isbn).order_by('id').first()
                            except Article.DoesNotExist:
                                article_id = None
                        else:
                            try:
                                row_object = Article.objects.get(pmid_isbn=pmid_isbn,first_page=pmid_isbn_page)
                            except Article.DoesNotExist:
                                article_id = None
                    else:
                        try:
                            row_object = Article.objects.filter(pmid_isbn=pmid_isbn).order_by('id').first()
                        except Article.DoesNotExist:
                            article_id = None
                    if row_object == None:
                        article_id = None
                    else:
                        article_id = row_object.id
                    if article_id == None:
                        # write new pmid_isbn to article_not_found
                        try:
                            row_object = article_not_found.objects.get(pmid_isbn=pmid_isbn)
                        except article_not_found.DoesNotExist:
                            row_object = article_not_found(pmid_isbn=pmid_isbn)
                            row_object.save()
                        try:
                            row_object = ingest_errors.objects.get(field='PMID/ISBN',value=pmid_isbn,file_row_num=row_num,filename='fp_fragment.csv')
                        except ingest_errors.DoesNotExist:
                            row_object = ingest_errors(field='PMID/ISBN',value=pmid_isbn,filename='fp_fragment.csv',file_row_num=row_num,comment='invalid pmid/isbn value')
                            row_object.save()
                #end set article_id
                # set type
                attachment      = None
                attachment_type = None
                type_fragment = 'data'
                

                # inits for both marker and ephys interpretation and linking info
                
                parameter              = None
                interpretation         = None
                interpretation_notes   = None
                linking_cell_id        = None
                linking_pmid_isbn      = None
                linking_pmid_isbn_page = None
                linking_quote          = None
                linking_page_location  = None
                
                # set interpretation
                try:
                    interpretation = row['Interpretation'].strip()
                    if len(interpretation) == 0:
                        interpretation = None
                except Exception:
                    interpretation = None
                # set interpretation_notes
                try:
                    interpretation_notes = row['Interpretation Notes'].strip()
                    if len(interpretation_notes) == 0:
                        interpretation_notes = None
                except Exception:
                    interpretation_notes = None
                # set linking_cell_id
                try:
                    parameter = row['Firing_Pattern'].strip()
                    if len(parameter) == 0:
                        parameter = None
                except Exception:
                    parameter = None
                try:
                    linking_cell_id = int(row['Linking Cell ID'].strip())
                except Exception:
                    linking_cell_id = None
                # set linking_pmid_isbn
                try:
                    linking_pmid_isbn = int(row['Linking PMID'].replace('-','').strip())
                except Exception:
                    linking_pmid_isbn = None
                # set linking_pmid_isbn_page
                try:
                    linking_pmid_isbn_page = int(row['Linking_pmid_isbn_page'].strip())
                except Exception:
                    linking_pmid_isbn_page = None
                # set linking_quote
                try:
                    linking_quote = row['Linking Quote'].strip()
                    if len(linking_quote) == 0:
                        linking_quote = None
                except Exception:
                    linking_quote = None
                # set linking_page_location
                try:
                    linking_page_location = row['Linking Quote Location'].strip()
                    if len(linking_page_location) == 0:
                        linking_page_location = None
                except Exception:
                    linking_page_location = None

                if reference_id != None:
                    # Fragment type = type
                    row_object = Fragment(
                        id                     = fragment_id,
                        original_id            = reference_id,
                        quote                  = material_used,
                        page_location          = location_in_reference,
                        pmid_isbn              = pmid_isbn,
                        pmid_isbn_page         = pmid_isbn_page,
                        cell_id                = cell_id,
                        type                   = type_fragment,
                        parameter              = parameter,
                        interpretation         = interpretation,
                        interpretation_notes   = interpretation_notes,
                        linking_cell_id        = linking_cell_id,
                        linking_pmid_isbn      = linking_pmid_isbn,
                        linking_pmid_isbn_page = linking_pmid_isbn_page,
                        linking_quote          = linking_quote,
                        linking_page_location  = linking_page_location
                    )
                    row_object.save()
                    fragment_id=row_object.id
                    row_object = Evidence()
                    row_object.save()
                    evidence_id=row_object.id
                    row_object = EvidenceFragmentRel(
                        Evidence_id = evidence_id,
                        Fragment_id = fragment_id
                    )
                    row_object.save()
                    evidence_id=row_object.id
                    row_object = ArticleEvidenceRel(
                        Article_id  = article_id,
                        Evidence_id = evidence_id
                    )
                    row_object.save()
                    fragment_id=fragment_id+1

            except Exception as e:
                if(reference_id!=None):
                    try:
                        row_object = ingest_errors.objects.get(file_row_num=row_num,filename='fp_fragment.csv')
                    except ingest_errors.DoesNotExist:
                        row_object = ingest_errors(filename='fp_fragment.csv',file_row_num=row_num,comment=str(e))
                        row_object.save()
                reference_id=None
            row_num=row_num+1
            
    # firing pattern parameters
    def parameters_to_parameters(self):
        row_num=2 
        for row in self.rows:
            type_id=None
            fig_no=None
            reference_id=None
            istim=None
            tstim=None
            firingPattern_id=None
            try:
                type_id=row['Uniq ID']
                type_id=int(type_id.replace('-',''))
                fig_no=row['Figure number']
                if(row['Reference ID'].strip()):
                    reference_id = row['Reference ID'].strip()
                    reference_id = int(reference_id)
                    try:
                        row_object = Fragment.objects.get(original_id=reference_id)
                    except Fragment.DoesNotExist:
                        try:
                            row_object = ingest_errors.objects.get(field='Reference ID',value=reference_id,filename='fp_parameters.csv')
                        except ingest_errors.DoesNotExist:
                            row_object = ingest_errors(field='Reference ID',value=reference_id,filename='fp_parameters.csv',file_row_num=row_num,comment='reference id value not found in fragment')
                            row_object.save()
                    istim=row['Istim (pA)']
                    tstim=row['Tstim (ms)']
                    firingPattern_id=FiringPatternStringField.firing_pattern_definition_parameter(row,'parameter')
                    row_object = FiringPatternRel(
                        FiringPattern_id    = firingPattern_id,
                        Type_id             = type_id,
                        figure_no           = fig_no,
                        original_id         = reference_id,
                        istim_pa            = istim,
                        tstim_ms            = tstim
                    )
                    row_object.save()
            except Exception as e:
                try:
                    row_object = ingest_errors.objects.get(file_row_num=row_num,filename='fp_parameters.csv')
                except ingest_errors.DoesNotExist:
                    row_object = ingest_errors(filename='fp_parameters.csv',file_row_num=row_num,comment=str(e))
                    row_object.save()
                type_id=None
                reference_id=None
                firingPattern_id=None
            row_num=row_num+1

    # firing pattern definition
    def definition_to_definition(self):
        cnt=0;
        row_num=4
        for row in self.rows:
            try:
                if(cnt>1):
                    FiringPatternStringField.firing_pattern_definition_parameter(row,'definition')
                cnt=cnt+1
                row_num=row_num+1
            except Exception as e:
                try:
                    row_object = ingest_errors.objects.get(file_row_num=row_num,filename='fp_definitions.csv')
                except ingest_errors.DoesNotExist:
                    row_object = ingest_errors(filename='fp_definitions.csv',file_row_num=row_num,comment=str(e))
                    row_object.save()
            row_num=row_num+1
    
    # helper function for importing firing pattern definitons and parameters 
    def firing_pattern_definition_parameter(row,parameter_value):
        overall_fp                          =row['OVERALL FIRING PATTERN']
        delay_ms                            =row['Delay (ms)']
        pfs_ms                              =row['PFS(ms)']
        swa_mv                              =row['SWA (mV)']
        nisi                                =row['NISI']
        isiav_ms                            =row['ISIAV (ms)']
        sd_ms                               =row['SD (ms)']
        max_isi_ms                          =row['Max ISI (ms)']
        min_isi_ms                          =row['Min ISI (ms)']
        first_isi_ms                        =row['1st ISI (ms)']
        isiav1_2_ms                         =row['ISIAV1-2  (ms)']
        isiav1_3_ms                         =row['ISIAV1-3 (ms)']
        isiav1_4_ms                         =row['ISIAV1-4 (ms)']
        last_isi_ms                         =row['Last ISI (ms)']
        isiavn_n_1_ms                       =row['ISIAVn-n-1 (ms)']
        isiavn_n_2_ms                       =row['ISIAVn-n-2 (ms)']
        isiavn_n_3_ms                       =row['ISIAVn-n-3 (ms)']
        maxisi_minisi                       =row['MaxISI/MinISI']
        maxisin_isin_m1                     =row['MaxISIn /ISIn-1']
        maxisin_isin_p1                     =row['MaxISIn /ISIn+1']
        ai                                  =row['AI = (ISIAVn-n-2 - ISIAV1-3)/ ISIAVn-n-2']
        rdmax                               =row['RDmax    (RDi=|ISIi-ISIAV|/ISIAV )']
        df                                  =row['DF=(Delay-2 ISIAV1-2)/Delay']
        sf                                  =row['SF=(PSF-2 ISIAVn-n-1)/PSF']
        tmax_scaled                         =row['Tmax(scaled)']
        isimax_scaled                       =row['ISImax(scaled)']
        isiav_scaled                        =row['ISIav (scaled)']
        sd_scaled                           =row['SD(scaled)']
        slope                               =row['Slope']
        intercept                           =row['Intercept']
        slope1                              =row['Slope1']
        intercept1                          =row['Intercept1']
        css_yc1                             =row['Css (Yc1)']
        xc1                                 =row['Xc1']
        slope2                              =row['Slope2']
        intercept2                          =row['Intercept2']
        slope3                              =row['Slope3']
        intercept3                          =row['Intercept3']
        xc2                                 =row['Xc2']
        yc2                                 =row['Yc2']
        f1_2                                =row['F1-2']
        f1_2crit                            =row['F1-2crit']
        f2_3                                =row['F2-3']
        f2_3crit                            =row['F2-3crit']
        f3_4                                =row['F3-4']
        f3_4crit                            =row['F3-4crit']
        p1_2                                =row['P1-2']
        p2_3                                =row['P2-3']
        p3_4                                =row['P3-4']
        p1_2uv                              =row['P1-2uv']
        p2_3uv                              =row['P2-3uv']
        p3_4uv                              =row['P3-4uv']
        isii_isii_m1                        =row['ISIi/ISIi-1']
        i                                   =row['i']
        isiav_i_n_isi1_i_m1                 =row['ISIav(i,n)/ISI1,i-1']
        maxisij_isij_m1                     =row['MaxISIj /ISIj-1']
        maxisij_isij_p1                     =row['MaxISIj /ISIj+1']
        nisi_c                              =row['NISI_c']
        isiav_ms_c                          =row['ISIAV (ms)_c']
        maxisi_ms_c                         =row['Max ISI (ms)_c']
        minisi_ms_c                         =row['Min ISI (ms)_c']
        first_isi_ms_c                      =row['1st ISI (ms)_c']
        tmax_scaled_c                       =row['Tmax(scaled) _c']
        isimax_scaled_c                     =row['ISImax(scaled)_c']
        isiav_scaled_c                      =row['ISIav (scaled) _c']
        sd_scaled_c                         =row['SD(scaled) _c']
        slope_c                             =row['Slope_c']
        intercept_c                         =row['Intercept_c']
        slope1_c                            =row['Slope1_c']
        intercept1_c                        =row['Intercept1_c']
        css_yc1_c                           =row['Css (Yc1) _c']
        xc1_c                               =row['Xc1_c']
        slope2_c                            =row['Slope2_c']
        intercept2_c                        =row['Intercept2_c']
        slope3_c                            =row['Slope3_c']
        intercept3_c                        =row['Intercept3_c']
        xc2_c                               =row['Xc2_c']
        yc2_c                               =row['Yc2_c']
        f1_2_c                              =row['F1-2_c']
        f1_2crit_c                          =row['F1-2crit_c']
        f2_3_c                              =row['F2-3_c']
        f2_3crit_c                          =row['F2-3crit_c']
        f3_4_c                              =row['F3-4_c']
        f3_4crit_c                          =row['F3-4crit_c']
        p1_2_c                              =row['P1-2_c']
        p2_3_c                              =row['P2-3_c']
        p3_4_c                              =row['P3-4_c']
        p1_2uv_c                            =row['P1-2uv_c']
        p2_3uv_c                            =row['P2-3uv_c']
        p3_4uv_c                            =row['P3-4uv_c']
        row_object = FiringPattern(
            overall_fp             =              overall_fp,            
            delay_ms               =              delay_ms,              
            pfs_ms                 =              pfs_ms,                
            swa_mv                 =              swa_mv,                
            nisi                   =              nisi,                  
            isiav_ms               =              isiav_ms,              
            sd_ms                  =              sd_ms,                 
            max_isi_ms             =              max_isi_ms,            
            min_isi_ms             =              min_isi_ms,            
            first_isi_ms           =              first_isi_ms,          
            isiav1_2_ms            =              isiav1_2_ms,           
            isiav1_3_ms            =              isiav1_3_ms,           
            isiav1_4_ms            =              isiav1_4_ms,           
            last_isi_ms            =              last_isi_ms,           
            isiavn_n_1_ms          =              isiavn_n_1_ms,         
            isiavn_n_2_ms          =              isiavn_n_2_ms,         
            isiavn_n_3_ms          =              isiavn_n_3_ms,         
            maxisi_minisi          =              maxisi_minisi,         
            maxisin_isin_m1        =              maxisin_isin_m1,       
            maxisin_isin_p1        =              maxisin_isin_p1,       
            ai                     =              ai,                    
            rdmax                  =              rdmax,                 
            df                     =              df,                    
            sf                     =              sf,                    
            tmax_scaled            =              tmax_scaled,           
            isimax_scaled          =              isimax_scaled,         
            isiav_scaled           =              isiav_scaled,          
            sd_scaled              =              sd_scaled,             
            slope                  =              slope,                 
            intercept              =              intercept,             
            slope1                 =              slope1,                
            intercept1             =              intercept1,            
            css_yc1                =              css_yc1,               
            xc1                    =              xc1,                   
            slope2                 =              slope2,                
            intercept2             =              intercept2,            
            slope3                 =              slope3,                
            intercept3             =              intercept3,            
            xc2                    =              xc2,                   
            yc2                    =              yc2,                   
            f1_2                   =              f1_2,                  
            f1_2crit               =              f1_2crit,              
            f2_3                   =              f2_3,                  
            f2_3crit               =              f2_3crit,              
            f3_4                   =              f3_4,                  
            f3_4crit               =              f3_4crit,              
            p1_2                   =              p1_2,                  
            p2_3                   =              p2_3,                  
            p3_4                   =              p3_4,                  
            p1_2uv                 =              p1_2uv,                
            p2_3uv                 =              p2_3uv,                
            p3_4uv                 =              p3_4uv,               
            isii_isii_m1           =              isii_isii_m1,          
            i                      =              i,                     
            isiav_i_n_isi1_i_m1    =              isiav_i_n_isi1_i_m1,   
            maxisij_isij_m1        =              maxisij_isij_m1,       
            maxisij_isij_p1        =              maxisij_isij_p1,       
            nisi_c                 =              nisi_c,                
            isiav_ms_c             =              isiav_ms_c,            
            maxisi_ms_c            =              maxisi_ms_c,           
            minisi_ms_c            =              minisi_ms_c,           
            first_isi_ms_c         =              first_isi_ms_c,        
            tmax_scaled_c          =              tmax_scaled_c,         
            isimax_scaled_c        =              isimax_scaled_c,       
            isiav_scaled_c         =              isiav_scaled_c,        
            sd_scaled_c            =              sd_scaled_c,           
            slope_c                =              slope_c,               
            intercept_c            =              intercept_c,           
            slope1_c               =              slope1_c,              
            intercept1_c           =              intercept1_c,          
            css_yc1_c              =              css_yc1_c,             
            xc1_c                  =              xc1_c,                 
            slope2_c               =              slope2_c,              
            intercept2_c           =              intercept2_c,          
            slope3_c               =              slope3_c,              
            intercept3_c           =              intercept3_c,          
            xc2_c                  =              xc2_c,                 
            yc2_c                  =              yc2_c,                 
            f1_2_c                 =              f1_2_c,                
            f1_2crit_c             =              f1_2crit_c,            
            f2_3_c                 =              f2_3_c,                
            f2_3crit_c             =              f2_3crit_c,            
            f3_4_c                 =              f3_4_c,                
            f3_4crit_c             =              f3_4crit_c,            
            p1_2_c                 =              p1_2_c,                
            p2_3_c                 =              p2_3_c,                
            p3_4_c                 =              p3_4_c,                
            p1_2uv_c               =              p1_2uv_c,              
            p2_3uv_c               =              p2_3uv_c,              
            p3_4uv_c               =              p3_4uv_c,              
            definition_parameter   =              parameter_value  
        )
        row_object.save()
        firing_pattern_id=row_object.id
        return firing_pattern_id
