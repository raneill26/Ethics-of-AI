# An Investigation Into Ethical Biases And Interpretations Of Generative Artificial Intelligence

## Abstract
As artificial intelligence systems become increasingly integrated into critical decision-making processes and everyday applications, understanding and mitigating bias remains a paramount ethical concern. This study investigates two central facets of bias within AI: image generation bias and moral reasoning bias, particularly in the context of the trolley problem. 

First, we examined how AI image models respond to prompts for various professional roles (e.g., executives, doctors, teachers, construction workers, and janitors), assessing potential disparities in gender representation and racial representation in the context of real-world statistics, equality, and equity. Applying three contemporary image generation AI models (DALL-E 3, Midjourney 6.1, and Stable Diffusion 3.5 Large Turbo), we have found that DALL-E 3 consistently under-represents masculine profiles in its images, whereas Midjourney 6.1 systematically overrepresents them. Stable Diffusion 3.5 strikes the best balance, wherein it does slightly skew male on the equity tests, but performs most closely with the actual distributions. Stable Diffusion 3.5 was found to mirror the actual population distributions of soldiers and mechanics, failing to reject the null hypothesis (AI masculine proportions are equal to the real world); and is in line with medical doctor distributions, making appropriate demographic percentage adjustments.

Second, we explored the moral dimension of AI bias by analyzing how large language models address classic trolley problem scenarios and the value of different lives. Our prompts altered the groups at risk and the actions required, allowing us to observe if the model’s decisions favor certain demographics or outcomes. We probed whether language models exhibit consistent ethical frameworks or if they produced unstable, context-dependent moral judgments that could be influenced by training data, cultural assumptions, and language preferences. Applying five contemporary image generation AI models (GPT-4, Gemini 2, DeepSeek V3, Perplexity, and Grok) we noticed the models exhibited a strong action bias, choosing to pull the lever the majority of the time. It should be noted that this contradicts the passivity that humans tend to exhibit when exposed to groups of equal value. 

The trolley problem results reflect a potential form of ethical fading wherein models disguise their actions of killing one group by reframing it as ‘saving another group’ when pulling the lever. Beyond this, each model revealed group-specific value judgements. Examples included privileging doctors, children, firefighters, women, etc. Although these systems assert value neutrality, after the decision is made, ad-hoc rationalization is applied with the appropriate ethical framework (deontological, consequential utilitarian, consequential egoist, etc.) to shield the AI’s judgment. This exposes biases likely stemming from the training data, which reflect that of general society.

## Collaborators
- Connor Hall  
- Maxime Dale  
- Ryan Neill  
- Halle Pearce  
- Joseph Reardon

## Findings
### 1. Image Generation Bias
- Across 45 profession–model combinations, no image generator achieved both demographic fidelity and gender neutrality.
- DALL·E 3:
    - Underrepresents masculine presentations in male-dominated roles
    - Favors lighter skin tones

- Midjourney 6.1:
    - Shows pronounced male bias and light skin prevalence

- Stable Diffusion 3.5:
    - Closest to real-world distributions for some professions
    - Still skews male and light-skinned overall

## Repo Contents
- EthicsOfGenerativeArtificialIntelligence.pdf: Full research paper
- LiteratureReviewPapers/: 
- Supplementary Data/
    - TrolleyData.pdf: Includes result statistics from Trolly Problem experiment
    - ImageGenerationScripts/: Includes three files used to generate image data
    - DataVisualization/: Includes scripts used to better illustrate data results into figures
    - ImageGenerationData/: Generated image data for each profession